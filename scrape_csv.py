# Web scraping script that downloads csv files in given static website
# TODO: (and optionally xlsx) add option to download xlsx files
import requests
import argparse
import urllib.robotparser as robotparser
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup
import lxml
# from pathlib import Path
import pathlib

# Note sure if I wanna run this as a standalone script or allow to be imported as a module
# class Scraper:
#     def __init__(self, website: str, output_dir: str):
#         self.website = website
#         self.output_dir = output_dir


def download_csv(url: str):
    print(url)

# if __name__ == "__main__":


# ======== Arg Parsing ======== #
parser = argparse.ArgumentParser(
    prog='CSV Web Scraper',
    description="Scrapes a website's csv files"
)
parser.add_argument('-w', '--website', help="Website's root URL. Format: 'scheme://netloc/'")
parser.add_argument('-o', '--output', help='output folder')

args = parser.parse_args()

# Access the values of the flags
website: str = args.website
if website is None:
    print("Usage is: scrape_csv.py -w <website> [-o <output directory>]")
    exit(1)

root_url: ParseResult = urlparse(website)
if not root_url.scheme in ['http', 'https']:
    print("-w website scheme should be 'http' or 'https'")
    exit(1)

output_folder: str = args.output if args.output is not None else root_url.netloc

# ======== Actual Crawling ======== #

if not website.endswith("/"):
    website += "/"
robots = requests.get(website + "robots.txt")

# Check if there is robots.txt
if robots.status_code != 200:
    print("Could not read "+website+"robots.txt. Status: "+robots.status_code)
    robots.raise_for_status()
    exit(1)

# Open output folder

pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

# Parse robots.txt
rp = robotparser.RobotFileParser()
rp.set_url(website + "robots.txt")
rp.read()
sitemaps = rp.site_maps()


# Parse sitemap.xml
for sitemap in set(sitemaps):
    # print(sitemap)
    sm = requests.get(sitemap)
    soup = BeautifulSoup(sm.text, 'xml')
    for url_tag in soup.find_all('loc'):
        url = url_tag.string
        download_csv(url)
        exit(1)