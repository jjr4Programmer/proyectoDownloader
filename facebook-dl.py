#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from tkinter import filedialog

import re
import sys
import requests
import urllib.request
import random
import argparse

good = "[✔]"

# This magic spell lets me erase the current line. 
# I can use this to show for example "Downloading..."
# and then "Downloaded" on the line where 
# "Downloading..." was.  
ERASE_LINE = '[*]'

# This extracts the video url
def extract_url(html, quality):

	if quality == "sd":
		# Standard Definition video
		url = re.search('sd_src:"(.+?)"', html)[0]
	else:
		# High Definition video
		url = re.search('hd_src:"(.+?)"', html)[0]

	# cleaning the url 
	url = url.replace('hd_src:"', '')
	url = url.replace('sd_src:"', '')
	url = url.replace('"', "")

	return url


def main():
	parser = argparse.ArgumentParser(description = "Download videos from facebook from your terminal")
	
	parser.add_argument('url', action="store")
	parser.add_argument('resolution', action="store", nargs="?")
	parser.add_argument('path', action="store")

	args = parser.parse_args()

	r = requests.get(args.url)

	file_url = extract_url(r.text, args.resolution)

	if len(args.path) > 4:
		# Downloads the video
		if not ".mp4" in args.path:
			args.path += ".mp4"
		urllib.request.urlretrieve(file_url, args.path)

if __name__=="__main__":
	main()