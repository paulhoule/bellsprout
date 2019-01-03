"""
Convert the intermediate file format into something truly efficient for database insertion

"""
import re
from pathlib import Path

from json import dumps, loads
import datetime
import dask.bag as db


class Rules:
    Href = re.compile(r'<a href="([^"]*)" ')
    Size = re.compile(r"(\d*)x(\d*) \(([^)]*)\)")

def recode(original_record):
    record = dict(original_record)
    tags = record.get("tags",[])
    record["tags"] = [t["name"] for t in tags]
    if "facts" not in record:
        return record

    facts = {f["property"]:f for f in record["facts"]}
    del record["facts"]
    del record["unknown_facts"]
    del record["unknown_tags"]
    if "Posted" in facts:
        record["posted_when"] = facts["Posted"]["value"]["when"]
        record["posted_by"] = facts["Posted"]["value"]["by_id"]
    if "Size" in facts:
        record["size_html"] = facts["Size"]["html"]
        link_match = Rules.Href.search(facts["Size"]["html"])
        if link_match:
            record["img_link"] = link_match.group(1)
        match = Rules.Size.match(facts["Size"]["value"])
        if match:
            record["width"] = match.group(1)
            record["height"] = match.group(2)
            record["approx_bytes"] = match.group(3)
    if "Source" in facts:
        record["source"] =facts["Source"]["value"]
    if "Rating" in facts:
        record["rating"] =facts["Rating"]["value"]
    if "Score" in facts:
        record["score"] = facts["Score"]["value"]
    if "Favorited by" in facts:
        ids = facts["Favorited by"]["value"]["ids"]
        fav_count = len(ids)
        if "#" in ids:
            last_name = facts["Favorited by"]["value"]["names"][-1]
            more_count = int(last_name.split(" ")[0])
            del ids[-1]
            fav_count = fav_count - 1 + more_count
        record["favorited_by"] = ids
        record["fav_count"] = fav_count
    if "Approver" in facts:
        record["approver"]=facts["Approver"]["value"]["id"]
    return record


in_dir = Path.home() / "5dbooru"
out_dir = Path.home() / "3db-final"
xxx = str(in_dir) + "/*.json.gz"

start = datetime.datetime.now()
all = db.read_text(xxx).map(loads).map(recode).map(dumps)
all.to_textfiles(str(out_dir) + "/image-*.json.gz")

end1 = datetime.datetime.now()


print(f"Run time is {end1-start}")
