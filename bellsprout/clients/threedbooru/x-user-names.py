from pathlib import Path

import yaml
from json import dumps, loads

from bellsprout.clients.threedbooru import read3d
import datetime
import dask.bag as db

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

def facts_with(record,property):
    if "facts" not in record:
        return []

    return [x["value"] for x in record["facts"] if x["property"]==property]

def tuplify_users(record):
    ids = []
    names = []
    favorited_by = facts_with(record,"Favorited by")
    for value in favorited_by:
        ids += value["ids"]
        names += value["names"]

    if ids and ids[-1] == '#':
        del ids[-1]
        del names[-1]

    posted = facts_with(record,"Posted")
    for value in posted:
        ids += [value["by_id"]]
        names += [value["by_name"]]
    for value in facts_with(record,"Approved"):
        ids += [value["id"]]
        names += [value["name"]]

    return set(zip(ids,names))

def unionizer(input):
    result = set()
    for x in input:
        result.update(x)
    return result

in_dir = Path.home() / "5dbooru"
xxx = str(in_dir) + "/*.json.gz"

start = datetime.datetime.now()
all = db.read_text(xxx).map(loads)
mappings = all.map(tuplify_users)

pairs = mappings.reduction(unionizer,unionizer).compute()
print(len(pairs))

with open(Path.home() / "3d-weeaboos.json","wt",encoding="utf-8") as type_out:
    for p in pairs:
        type_out.write(dumps(dict(_key=p[0], name=p[1])))
        type_out.write('\n')

end1 = datetime.datetime.now()


print(f"Run time is {end1-start}")
