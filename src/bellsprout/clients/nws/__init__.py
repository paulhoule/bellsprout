import datetime

import logging
import re
from logging import getLogger, basicConfig
from math import floor
from pathlib import Path

import imageio
import requests
from bs4 import BeautifulSoup

_logger = getLogger(__package__)
basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.ERROR)

# 600 x 576

class RadarFetch():
    def __init__(self):
        self._session = requests.Session()
        self._source_base = "https://radar.weather.gov/"
        self._destination_dir = Path.home() / "radar"

        self._patterns = [
            "ridge/RadarImg/N0R/BGM/BGM_[0-9]{8}_[0-9]{4}_N0R.gif",
            "Conus/RadarImg/northeast_[0-9]{8}_[0-9]{4}.gif"
        ]


    def refresh(self):
        self._session = requests.Session()
        for pattern in self._patterns:
            self._refresh(pattern)

    def _refresh(self,pattern):
        product_dir = "/".join(pattern.split("/")[:-1])
        regex = re.compile(pattern.split("/")[-1])
        target_dir = self._destination_dir / product_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        url_directory = self._source_base + product_dir + "/"
        _logger.warning(f"Checking {url_directory}")
        target = self._session.get(url_directory).text
        soup = BeautifulSoup(target,features="lxml")
        links = soup.find_all("a")
        crawl = []
        for link in links:
            href = link["href"]
            if regex.match(href):
                crawl.append(href)

        for href in crawl:
            target_file = self._destination_dir / product_dir / href
            _logger.debug(f"Checking for local {target_file}")
            if target_file.exists():
                _logger.debug(f"File already exists -- no need to download {href}")
            else:
                _logger.warning(f"Downloading {href}")
                gif_data = self._session.get(url_directory + href)
                if gif_data.ok and gif_data.content:
                    with open(target_file,"wb") as FILE:
                        pass
                        FILE.write(gif_data.content)

f = RadarFetch()
f.refresh()

now = datetime.datetime.now(datetime.timezone.utc)
window = datetime.timedelta(days=2)

src = Path.home() / "radar/Conus/RadarImg"
infiles = sorted(src.glob("*.gif"))
file_pattern=re.compile(r"_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2}).gif$")

def date_from_filename(name):
    match = file_pattern.search(name)
    if not match:
        return None

    (year,month,day,hour,minute) = map(int,match.groups())
    return datetime.datetime(year,month,day,hour,minute, tzinfo=datetime.timezone.utc)

dated = [{"path": file,"timestamp": date_from_filename(file.name)}for file in infiles]
dated = [{**row, "age":now-row["timestamp"]} for row in dated if row["timestamp"]]
dated = [row for row in dated if row["age"]<window]

processed = Path("/var/www/html/radar/")
processed.mkdir(parents=True,exist_ok=True)
with imageio.get_writer(
        str(processed / "northeast.mp4"),
        mode='I',fps=10) as writer:
    for item in dated:
        file = item["path"]
        try:
            content = imageio.imread(str(file))
        except ValueError as err:
            print(str(type(err)) + ":" + str(err))
            print("Could not read image from "+str(file)+" deleting")
            try:
                # if the file is corrupt ignore it and get rid of it
                file.unlink()
                # on Windows the file might not have been released by imageio and we might
                # not be able to delete it
            except PermissionError:
                pass
            continue

        # the image should be divisible for 16x16 macroblocks;  crop away the from the left
        # and the top because my judgement is that for the northeast case this is best.
        (width,height,channels) = content.shape
        legal_width = 16*floor(width/16)
        legal_height= 16*floor(height/16)
        cropped = content[-legal_width:,-legal_height:]

        writer.append_data(cropped)