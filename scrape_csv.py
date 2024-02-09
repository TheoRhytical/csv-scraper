# Web scraping script that downloads csv files in given static website
# TODO: (and optionally xlsx) add option to download xlsx files
import argparse

parser = argparse.ArgumentParser(
    prog='CSV Web Scraper',
    description="Scrapes a website's csv files"
)
parser.add_argument('-w', '--website', help="Website's root URL")
parser.add_argument('-o', '--output', help='output folder')

args = parser.parse_args()

# Access the values of the flags
website = args.website
output_folder = args.output
