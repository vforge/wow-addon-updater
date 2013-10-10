# coding: utf-8

import sys
import os
import requests
from libs.WowAddons import WowAddons
from libs.WowUtils import WowUtils
from libs.WowAddonsRepository import WowAddonsRepository

def sep(style = '-'):
	print(style * 30)

def step0_title():
	sep("=")
	print("WoW Addon Updater")
	sep()

def step1_scan():
	directory = 'AddOnsSample'
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	print("STEP 1: Scanning %s" % directory)
	sep()
	addons = WowAddons(directory)
	sep()
	return addons

def step2_get_archives(addons):
	counter, size, links = 0, len(addons.addons), []
	print("STEP 2: Finding archives")
	sep()
	for addon in addons.addons:
		counter += 1
		print("%d/%d: %s" % (counter, size, addon.name))
		try:
			repository = WowAddonsRepository.factory(addon)
			links.append(repository.get_downloading_link(addon))
		except ValueError:
			print("Cannot find source for that :(")
		finally:
			sep()
	return links
	
def download_file(url, directory):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(directory + '/' + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename
	
def step3_download_zips(links):
	print("STEP 3: Downloading archives")
	sep()
	# create dir
	directory = 'downloaded'
	if not os.path.exists(directory):
		os.makedirs(directory)
	# download zips
	for url in links:
		print(url)
		download_file(url, directory)

# main functions
step0_title()
addons = step1_scan()
links = step2_get_archives(addons)
step3_download_zips(links)
