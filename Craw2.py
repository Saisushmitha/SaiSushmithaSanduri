# used to process one file at a time

import re
import requests
import sys
from warcio.archiveiterator import ArchiveIterator



regex = re.compile(r"covid.*(economic.*impact|impact.*economic|pandemic.*economic.*impact|economic.*impact.*pandemic|pandemic.*impact.*economic|impact.*pandemic.*economic)", re.IGNORECASE | re.DOTALL)

entries = 0
matching_entries = 0

file_name = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-50/segments/1606141163411.0/warc/CC-MAIN-20201123153826-20201123183826-00032.warc.gz"

if len(sys.argv) > 1:
    file_name = sys.argv[1]

stream = None
if file_name.startswith("http://") or file_name.startswith(
    "https://"
):
    stream = requests.get(file_name, stream=True).raw
else:
    stream = open(file_name, "rb")

results = []

for record in ArchiveIterator(stream):
    if record.rec_type == "warcinfo":
        continue

    if not ".com/" in record.rec_headers.get_header(
        "WARC-Target-URI"
    ):
        continue

    entries = entries + 1
    contents = (
        record.content_stream()
        .read()
        .decode("utf-8", "replace")
    )
    if regex.search(contents):
        matching_entries = matching_entries + 1
        results.append(record.rec_headers.get_header("WARC-Target-URI"))

# print("{} matching pages found in {}/{} entries.".format(len(results), matching_entries, entries))
for url in results:
    print(url)
