from pathlib import Path

import yaml
from arango import ArangoClient
from json import dumps

from bellsprout.clients.threedbooru import find_files,read3d
import datetime
import dask.bag as db

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

client = ArangoClient(**config["nemesis"]["client"])
adb = client.db(**config["nemesis"]["database"])
collection = adb.collection("post")

def insert_partition(group):
    return dumps(list(group))

def read3d_or_bust(filename):
    try:
        return read3d(filename)
    except:
        return {
            "_key": str(filename).split(".")[0],
            "message": "could not parse!"
        }

files = find_files()
files = db.from_sequence(files,partition_size=1000)

out_dir = Path.home() / "5dbooru"


start = datetime.datetime.now()
all = files.map(read3d_or_bust)
all = all.map(dumps)
# that = all.map_partitions(insert_partition)
all.to_textfiles(str(out_dir) + "/*.json.gz")
end1 = datetime.datetime.now()


print(f"Run time is {end1-start}")