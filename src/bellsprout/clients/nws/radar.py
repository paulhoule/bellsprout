import datetime
import re

from bellsprout.clients.nws import RadarFetch


def radar_file_date(name):
    file_pattern = re.compile(r"_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(?:_N0R|_N1P)?.gif$")
    match = file_pattern.search(name)
    if not match:
        return None

    (year, month, day, hour, minute) = map(int, match.groups())
    return datetime.datetime(year, month, day, hour, minute, tzinfo=datetime.timezone.utc)

f = RadarFetch(
    "https://radar.weather.gov/",
    [
        dict(
            pattern = "ridge/RadarImg/N0R/BGM/BGM_[0-9]{8}_[0-9]{4}_N0R.gif",
            date_fn = radar_file_date,
            video = "N0RBGM.mp4"
        ),
        dict(
            pattern="ridge/RadarImg/N1P/BGM/BGM_[0-9]{8}_[0-9]{4}_N1P.gif",
            date_fn=radar_file_date,
            video="N1PBGM.mp4"
        ),
        dict(
            pattern = "Conus/RadarImg/northeast_[0-9]{8}_[0-9]{4}.gif",
            date_fn = radar_file_date,
            video = "northeast.mp4"
        )
]
)
f.refresh()
f.make_video()