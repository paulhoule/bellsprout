from pathlib import Path

import yaml
from arango import ArangoClient

from bellsprout.clients.threedbooru import find_files,read3d
import datetime
import dask.bag as db

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

client = ArangoClient(**config["nemesis"]["client"])
adb = client.db(**config["nemesis"]["database"])
collection = adb.collection("post")

def insert_partition(group):
    collection.insert_many(list(group))

files = find_files()
files = db.from_sequence(files)

start = datetime.datetime.now()
all = files.map(read3d)
that = all.map_partitions(insert_partition)
that.compute()
end1 = datetime.datetime.now()


print(f"Run time is {end1-start}")