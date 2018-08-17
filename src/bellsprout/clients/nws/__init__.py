import logging
import re
import time
from logging import getLogger, basicConfig
from pathlib import Path
import requests
from bs4 import BeautifulSoup

_logger = getLogger(__package__)
basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.ERROR)

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
                _logger.warn(f"Downloading {href}")
                gif_data = self._session.get(url_directory + href)
                with open(target_file,"wb") as FILE:
                    FILE.write(gif_data.content)

f = RadarFetch()
f.refresh()
