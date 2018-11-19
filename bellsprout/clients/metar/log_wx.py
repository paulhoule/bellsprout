import yaml
from pathlib import Path
from arango import ArangoClient, DocumentInsertError

from bellsprout.clients.metar import get_metar

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

client = ArangoClient(**config["adb"]["client"])
db = client.db(**config["adb"]["database"])
collection = db.collection("metar")

airport = "KITH"
metar = get_metar(airport)
try:
    collection.insert(metar,silent=True)
except DocumentInsertError:
    pass
