from pathlib import Path

import yaml
from arango import ArangoClient
import json
import dask.bag as db

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

client = ArangoClient(**config["nemesis"]["client"])
adb = client.db(**config["nemesis"]["database"])
post = adb.collection("post")

in_dir = Path.home() / "3db-final"
xxx = str(in_dir) + "/image-*.json.gz"

def insert_partition(group):
    post.insert_many(list(group))


#results = db.read_text(xxx).map(json.loads).map_partitions(insert_partition)
#results.compute()

db.read_text(in_dir/"3d-types.json").map(json.loads).map(adb.collection("tag").insert).compute()
db.read_text(in_dir/"3d-weeaboos.json").map(json.loads).map(adb.collection("weeaboo").insert).compute()