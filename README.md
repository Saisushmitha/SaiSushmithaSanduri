# COVID-19 Economic Impact Crawler

## Description
This program uses the Common Crawl archive to find web pages that are relevant to the COVID-19 pandemic's economic impact. The program is written in Python and makes use of the requests and warctools packages to retrieve and extract text from the WARC files in the Common Crawl archive. The program uses a regex pattern to search for relevant web pages and saves the URLs and text content to a file for further analysis.

## Requirements
To run this program, you will need the following software and packages installed:
Python 3.x
Requests (pip install requests)
Warctools (pip install warctools)

## Usage
Clone or download the repository to your local machine.
Navigate to the directory where the program is located.
Run the program using the following command: `python Crawler.py > output.txt`
The program will take some time to complete, depending on the number of WARC files to process.
The resulting URLs and text content will be saved to a file named `output.txt` in the same directory as the program.
The output is present in Nov_Dec_2020 and in Feb_2020

## Approach 
The base code for processing of the webrc file is from [1] these files for every month on the Comman Crawler are present in webrc.path.gz file which encapsulates webrc.gz links. 
After testing many different variations of the regex expressions as present in comments in Crawler.py 
The below regex contains matches to extracting all the covid economy  related data is 
 `covid.(economic.(impact|crisis)|(impact|crisis).economic|pandemic.(econom(y|ic)|economic.*impact))", re.IGNORECASE | re.DOTALL`
This regex will match any occurrences of the words "covid", "economic", "impact", and "pandemic" in any order and combination, as long as they are present in the text being searched. The re.IGNORECASE flag makes the search case-insensitive, and re.DOTALL makes the dot (.) in the regex match any character, including newline character

## Findings:

1. there are URLs in the extarated output whihc are currrent not avaible giving a 404 error
2. There are many synomysly words used for economic impact and covid  which have not been considered in depth
3. On an average the number of warc files in each path is 30,000. The time required to process one path file takes more than an hour so much more processing power is required and using Mapreduce in this case would be much helpful


References:
[1] https://github.com/code402/warc-benchmark/blob/master/python/go.py
[2] https://arxiv.org/pdf/2102.09507

