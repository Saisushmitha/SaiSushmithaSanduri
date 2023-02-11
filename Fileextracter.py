import requests
import gzip
from io import BytesIO


url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-50/warc.paths.gz"
response = requests.get(url)

with gzip.open(BytesIO(response.content), "rb") as f:
    content = f.read()

warc_paths = content.decode("utf-8").split("\n")
for path in warc_paths:
        print(path)
