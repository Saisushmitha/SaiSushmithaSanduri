# Crawler.py
# This program is a Python script that retrieves and processes web pages from the Common Crawl archive that are relevant to the economic impact of COVID-19 or the pandemic. The program uses the requests library to download and extract WARC files from the Common Crawl archive and then filters the pages using a regular expression pattern. The regular expression pattern matches pages that contain the terms "covid," "economic," and "impact" (in any order) and is flexible to match different variations and spelling of these terms.

import re
import requests
import sys
from warcio.archiveiterator import ArchiveIterator
from io import BytesIO
import gzip

# Below are the regex being considered and tested against 
#consider this number 1
# regex = re.compile(r"covid.*(economi|economic).*", re.IGNORECASE | re.DOTALL)

# Provides better results than number 1 #2
# regex = re.compile(r"covid.*(economic.*impact|impact.*economic)", re.IGNORECASE | re.DOTALL)

# trying with this one #3
# regex = re.compile(r"covid.*(\beconom.*\b)", re.IGNORECASE | re.DOTALL)

# regex = re.compile(r"covid.*(economic.*impact|impact.*economic|pandemic.*economic.*impact|economic.*impact.*pandemic|pandemic.*impact.*economic|impact.*pandemic.*economic)", re.IGNORECASE | re.DOTALL)

regex = re.compile(r"covid.(economic.(impact|crisis)|(impact|crisis).economic|pandemic.(econom(y|ic)|economic.*impact))", re.IGNORECASE | re.DOTALL)

entries = 0
matching_entries = 0

# base URL for all the warc.gz
base_url = "https://data.commoncrawl.org/"

# considering for nov-dec months
# warc_paths_url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-50/warc.paths.gz"

# jan-2020 data
warc_paths_url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-05/warc.paths.gz"
response = requests.get(warc_paths_url)
with gzip.open(BytesIO(response.content), "rb") as f:
    warc_paths = f.read().decode("utf-8").split("\n")

results = []
for warc_path in warc_paths:
    if len(warc_path) == 0:
        continue
    full_url = base_url + warc_path
    stream = requests.get(full_url, stream=True).raw
    for record in ArchiveIterator(stream):
        if record.rec_type == "warcinfo":
            continue

        if not ".com/" in record.rec_headers.get_header("WARC-Target-URI"):
            continue

        entries = entries + 1
        contents = (
            record.content_stream().read().decode("utf-8", "replace")
        )
        if regex.search(contents):
            matching_entries = matching_entries + 1
            results.append(record.rec_headers.get_header("WARC-Target-URI"))
    

# print("{} matching pages found in {}/{} entries.".format(len(results), matching_entries, entries))
for url in results:
    print(url)
