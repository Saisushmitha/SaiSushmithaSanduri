import re
import requests
import sys
from warcio.archiveiterator import ArchiveIterator
from io import BytesIO
import gzip

# regex = re.compile(r"covid.*economic.*impact", re.IGNORECASE)
# regex = re.compile(r"covid", re.IGNORECASE | re.DOTALL)

#consider this number 1
# regex = re.compile(r"covid.*(economi|economic).*", re.IGNORECASE | re.DOTALL)

# Provides better results than number 1 #3
# regex = re.compile(r"covid.*(economic.*impact|impact.*economic)", re.IGNORECASE | re.DOTALL)

# trying with this one #3
# regex = re.compile(r"covid.*(\beconom.*\b)", re.IGNORECASE | re.DOTALL)
# Getting only the covid ones
regex =re.compile(r"covid", re.IGNORECASE | re.DOTALL) 


entries = 0
matching_entries = 0
base_url = "https://data.commoncrawl.org/"

warc_paths_url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-50/warc.paths.gz"
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
    break

print("{} matching pages found in {}/{} entries.".format(len(results), matching_entries, entries))
for url in results:
    print(url)
