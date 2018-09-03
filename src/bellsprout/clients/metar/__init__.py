import math

from metar import Metar
import requests

airport="KITH"

session=requests.Session()
def get_metar(airport):
    stations = f"http://tgftp.nws.noaa.gov/data/observations/metar/stations/"
    url = f"{stations}/{airport}.TXT"
    text = session.get(url).text
    parts = text.split('\n')
    return parts[1]

def rel_humidity(temp,dewpt):
    return 100.0 * (math.exp((17.625 * dewpt) / (243.04 + dewpt)) /
                    math.exp((17.625 * temp) / (243.04 + temp)))

def internal_metar(wxd):
    document = {}
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


    # if self.press:
    #     lines.append("pressure: %s" % self.press.string("mb"))
    # if self.weather:
    #     lines.append("weather: %s" % self.present_weather())
    # if self.sky:
    #     lines.append("sky: %s" % self.sky_conditions("\n     "))
    # if self.press_sea_level:
    #     lines.append("sea-level pressure: %s" % self.press_sea_level.string("mb"))
    # if self.max_temp_6hr:
    #     lines.append("6-hour max temp: %s" % str(self.max_temp_6hr))
    # if self.max_temp_6hr:
    #     lines.append("6-hour min temp: %s" % str(self.min_temp_6hr))
    # if self.max_temp_24hr:
    #     lines.append("24-hour max temp: %s" % str(self.max_temp_24hr))
    # if self.max_temp_24hr:
    #     lines.append("24-hour min temp: %s" % str(self.min_temp_24hr))
    # if self.precip_1hr:
    #     lines.append("1-hour precipitation: %s" % str(self.precip_1hr))
    # if self.precip_3hr:
    #     lines.append("3-hour precipitation: %s" % str(self.precip_3hr))
    # if self.precip_6hr:
    #     lines.append("6-hour precipitation: %s" % str(self.precip_6hr))
    # if self.precip_24hr:
    #     lines.append("24-hour precipitation: %s" % str(self.precip_24hr))
    # if self._remarks:
    #     lines.append("remarks:")
    #     lines.append("- " + self.remarks("\n- "))
    # if self._unparsed_remarks:
    #     lines.append("- " + ' '.join(self._unparsed_remarks))


