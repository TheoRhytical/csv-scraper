# Web scraping script that downloads csv files in given static website
# TODO: (and optionally xlsx) add option to download xlsx files
import requests
import argparse
import urllib.robotparser as robotparser
from bs4 import BeautifulSoup
import lxml

# Note sure if I wanna run this as a standalone script or allow to be imported as a module
# class Scraper:
#     def __init__(self, website: str, output_dir: str):
#         self.website = website
#         self.output_dir = output_dir

# if __name__ == "__main__":


# ======== Arg Parsing ======== #
parser = argparse.ArgumentParser(
    prog='CSV Web Scraper',
    description="Scrapes a website's csv files"
)
parser.add_argument('-w', '--website', help="Website's root URL")
parser.add_argument('-o', '--output', help='output folder')

args = parser.parse_args()

# Access the values of the flags
website: str = args.website
output_folder: str = args.output

# ======== Actual Crawling ======== #

if not website.endswith("/"):
    website += "/"
robots = requests.get(website + "robots.txt")

# Check if there is robots.txt
if robots.status_code != 200:
    print("Could not read "+website+"robots.txt")
    exit

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
    for url in soup.find_all('loc'):
        print(url)
