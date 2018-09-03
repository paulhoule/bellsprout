import datetime
import re

from bellsprout.clients.nws import RadarFetch

def sat_file_date(name):
    file_pattern=re.compile(r"^(\d{4})(\d{3})(\d{2})(\d{2})_")
    match = file_pattern.search(name)
    if not match:
        return None

    (year, day_in_year, hour, minute) = map(int, match.groups())
    first_day = datetime.datetime(year, 1, 1,hour,minute,tzinfo=datetime.timezone.utc)
    return first_day + datetime.timedelta(day_in_year)


g = RadarFetch(
    "https://cdn.star.nesdis.noaa.gov/",
    [dict(
        pattern = "GOES16/ABI/SECTOR/ne/GEOCOLOR/\d{11}_GOES16-ABI-ne-GEOCOLOR-1200x1200.jpg",
        date_fn = sat_file_date,
        video = "northeast-color.mp4"
    )]
)
g.refresh()
g.make_video()

