from pathlib import Path

import yaml
from json import dumps, loads

from bellsprout.clients.threedbooru import read3d
import datetime
import dask.bag as db

config_file = Path.home() / ".bellsprout" / "config.yaml"
config = yaml.load(config_file.open("r"))

def tuplify(tags):
    return {(x['name'],x['class']) for x in tags}

def unionizer(input):
    result = set()
    for x in input:
        result.update(x)
    return result

in_dir = Path.home() / "5dbooru"
xxx = str(in_dir) + "/*.json.gz"

start = datetime.datetime.now()
all = db.read_text(xxx).map(loads)
mappings = all.pluck("tags",default=set()).map(tuplify)

pairs = mappings.reduction(unionizer,unionizer).compute()

print()
with open(Path.home() / "3d-types.json","wt",encoding="utf-8") as type_out:
    for p in pairs:
        type_out.write(dumps(dict(_key=p[0], tag_type=p[1])))
        type_out.write('\n')

end1 = datetime.datetime.now()


print(f"Run time is {end1-start}")
