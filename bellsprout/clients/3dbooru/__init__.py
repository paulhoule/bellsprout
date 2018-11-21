from pathlib import Path
from random import choices
from time import sleep
from os import listdir
import gzip

import requests

where = Path.home() / "3dbooru"
upper_bound = 641067
sample_size = 25000

if not where.exists():
    where.mkdir(parents=True)

population = set(range(upper_bound))
i_have = {int(x.split('.')[0]) for x in listdir(where)}

crawl_list = choices(list(population-i_have), k=sample_size)



headers = {
    "User-Agent": "Kyubey 33.7 (have been using up spares)"
}

for x in crawl_list:
   sleep(1)
   url = f"http://behoimi.org/post/show/{x}"
   try:
       print("Fetching "+url)
       result = requests.get(url, headers=headers)
       if result.status_code==200:
           with gzip.open(where / f"{x}.html.gz","wt") as OUTPUT:
            OUTPUT.write(result.text)
       else:
           print(f"** anomalous status code {result.status_code}")
   except Exception as x:
       print(x)
