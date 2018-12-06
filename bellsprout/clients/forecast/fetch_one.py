from requests import get
import xml.etree.ElementTree as ET
import pandas as pd

target_url = "https://forecast.weather.gov/MapClick.php?lat=42.3643&lon=-76.3379&FcstType=digitalDWML"
xml = ET.fromstring(get(target_url).content)
head, data = xml

time_indices = {}

def convert_times(layout,name):
    out = []
    for item in layout.iter(name):
        out += [item.text]
    return pd.Series(out,dtype="[datetime64[ns, US/Eastern]")

BILLION = 1000000000
intervals = [
    ("D", 24*3600),
    ("h", 3600),
    ("m", 60),
    ("s", 1),
]

def toFreq(timedelta):
    clicks = int(timedelta)
    if clicks % BILLION:
        return None

    sec = clicks / BILLION
    for code, amount in intervals:
        if sec % amount == 0:
            return code

def equal_as_ordered(x,y):
    bool_vector = (x.reset_index(drop=True) == y.reset_index(drop=True))
    return bool_vector.all()

for layout in data.iter("time-layout"):
    key = next(layout.iter("layout-key")).text

    start_valid_time = convert_times(layout, 'start-valid-time')
    end_valid_time = convert_times(layout, 'end-valid-time')
    time_indices[key] = {
        "start-valid-time": start_valid_time,
        "end-valid-time": end_valid_time,
    }

    f1 = pd.infer_freq(start_valid_time.astype("datetime64"))
    f2 = pd.infer_freq(end_valid_time.astype("datetime64"))

    if f1 != f2:
        continue

    if not equal_as_ordered(start_valid_time[1:],end_valid_time[:-1]):
        continue

    time_indices[key]["index"] = pd.PeriodIndex(start_valid_time,freq=f1)

series = {}
for parameters in data.iter("parameters"):
    for parameter in parameters:
        tag_name = parameter.tag
        time_layout = parameter.attrib["time-layout"]
        if "index" not in time_indices[time_layout]:
            print(f"Could not create PeriodIndex for layout {time_layout}")
            break

        typus = parameter.get("type",None)
        if typus:
            whole_name = tag_name + "/" + typus
        else:
            whole_name = tag_name

        points = []
        for point in parameter:
            if point.tag == "value":
                if point.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}nil"):
                    points += [ None ]
                else:
                    points += [ point.text ]

        index = time_indices[time_layout]["index"]
        if len(points) != len(index):
            print(f"Couldn't find enough points to match index for {whole_name}")
            break


        series[whole_name] = pd.Series(points,index=index,dtype="float")




#    delta = end_valid_time - start_valid_time
#    periods = delta.unique()
#    if len(periods) == 1:
#        print (toFreq(periods))


