import time
from collections import namedtuple
from typing import List

import requests
from lxml import etree

Abstract = namedtuple("Abstract",["title","link","description"])

class PubmedQuery:
    ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self,term):
        self.db="pubmed"
        self.term=term

    def query(self, start):
        start_time = time.time()
        result = requests.get(PubmedQuery.ESEARCH, params={
            "db": self.db,
            "term": self.term,
            "retstart": start,
            "retmax": 1000,
        })
        finish = time.time()
        print(f"Elapsed time: {finish-start_time}")

        parse_start=time.time()
        try:
            xml = etree.fromstring(result.content)
            return xml.xpath("//IdList/Id/text()")
        finally:
            parse_end=time.time()
            print(f"Parse time: {parse_end-parse_start}")

    def fetch(self, id: List[str],retmode,rettype):
        start = time.time()
        result = requests.get(PubmedQuery.EFETCH, params={
            "db": self.db,
            "term": self.term,
            "id": ",".join(id),
            "retmode": retmode,
            "rettype": rettype,
        })
        finish = time.time()

        print(f"Elapsed time : {finish-start}")

        return result.content

