import yaml
from pathlib import Path
from arango import ArangoClient, DocumentInsertError

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

client = ArangoClient(**config["adb"]["client"])
db = client.db(**config["adb"]["database"])
collection = db.collection("metar")

collection.add_skiplist_index(["station","time"])