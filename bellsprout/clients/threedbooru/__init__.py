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

    post_id = None
    for element in soup.select('#stats ul li'):
        try:
            text = element.text
            parts = list(map(lambda s:s.strip(), text.split(":",maxsplit=1)))
            key = parts[0]
            value = parts[1]
            html = str(element)
            if key == "Id":
                post_id = value
                value = int(value)
                html = None
            elif key == "Posted":
                links = element.find_all("a")
                value = {
                    "when": links[0]["title"],
                    "by_id": int(links[1]["href"].split("/")[-1]),
                    "by_name": links[1].text
                }
            fact = {
                "property": key,
                "value": value
            }

            if html:
                fact["html"] = html

            facts += [fact]
        except CantParseTagException:
            unknown_facts += [str(element)]


    return {
        "_key": post_id,
        "tags": tags,
        "facts": facts,
        "unknown_tags": unknown_tags,
        "unknown_facts": unknown_facts
    }