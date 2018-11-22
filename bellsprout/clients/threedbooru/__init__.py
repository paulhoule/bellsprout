import gzip
from pathlib import Path
from bs4 import BeautifulSoup


def find_files():
    where = Path.home() / "3dbooru"
    files = list(where.glob("*.gz"))
    return files


class CantParseTagException(Exception):
    pass


def read3d(filename):
    with gzip.open(filename,"rb") as HTML:
        soup = BeautifulSoup(HTML,features="lxml")

    tags = []
    unknown_tags = []
    for element in soup.select('#tag-sidebar li'):
        try:
            clazz = element["class"][0]
            links = element.select("a")
            local_tags = set()
            for link in links:
                href = link["href"]
                parts = href.split("=")
                tagname = parts[1]
                local_tags.add(tagname)

            if len(local_tags) == 1:
                member = list(local_tags)[0]
                tags += [{"class": clazz, "name": member}]
            else:
                raise CantParseTagException("Couldn't parse tag")

        except CantParseTagException:
            unknown_tags += [str(element)]

    facts = []
    unknown_facts = []

    for element in soup.select('#stats ul li'):
        unknown_facts += [str(element)]

    return {"tags": tags,
            "facts": facts,
            "unknown_tags": unknown_tags,
            "unknown_facts": unknown_facts
            }