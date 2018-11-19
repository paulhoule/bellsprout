import math

from metar.Metar import Metar
import requests

session=requests.Session()
def get_metar(airport):
    stations = f"http://tgftp.nws.noaa.gov/data/observations/metar/stations/"
    url = f"{stations}/{airport}.TXT"
    text = session.get(url).text
    parts = text.split('\n')
    metar = internal_metar(parts[1])
    assign_key(metar)
    return metar

def rel_humidity(temp,dewpt):
    return 100.0 * (math.exp((17.625 * dewpt) / (243.04 + dewpt)) /
                    math.exp((17.625 * temp) / (243.04 + temp)))

def internal_metar(metar_text):
    document = {}
    wxd = Metar(metar_text)
    document["station"] = wxd.station_id

    if wxd.type:
        document["type"] = wxd.type

    if wxd.time:
        document["time"] = wxd.time.isoformat()+'Z'

    if wxd.temp:
        document["temp"] = wxd.temp.value(units="F")

    if wxd.dewpt:
        document["dewpt"] = wxd.dewpt.value(units="F")

    if "temp" in document and "dewpt" in document:
        document["humidity"] = rel_humidity(document["temp"],document["dewpt"])

    if wxd.wind_speed:
        document["wind_speed"] = wxd.wind_speed.value(units="mph")

    if wxd.wind_dir:
        document["wind_dir"] = wxd.wind_dir.value()

    if wxd.vis:
        document["visibility"] = wxd.vis.value(units="sm")

    if wxd.press:
        document["pressure"] = wxd.press.value(units="mb")

    if wxd.sky:
        document["sky"] = wxd.sky_conditions()

    if wxd.press_sea_level:
        document["pressure"] = wxd.press_sea_level.value("mb")

    document["code"] = wxd.code

    return document

def assign_key(metar_data):
    parts = metar_data["code"].split(" ")
    metar_data["_key"] = metar_data["station"] + '-' + '201811' + '-' + parts[1]