# coding: utf-8

import sys
from libs.WowAddons import WowAddons
from libs.Utils import Utils
from libs.WowAddonsRepository import WowAddonsRepository


def step0_title():
	Utils.sep("=")
	print("WoW Addon Updater")
	Utils.sep()


def step1_scan():
	directory = 'AddOnsSample'
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	print("STEP 1: Scanning %s" % directory)
	Utils.sep()
	addons = WowAddons(directory)
	Utils.sep()
	return addons


def step2_get_archives(addons):
	counter, size, links = 0, len(addons.addons), []
	print("STEP 2: Finding archives")
	Utils.sep()
	for addon in addons.addons:
		counter += 1
		print("%d/%d: %s" % (counter, size, addon.name))
		try:
			repository = WowAddonsRepository.factory(addon)
			links.append(repository.get_downloading_link(addon))
		except ValueError:
			print("Cannot find source for that :(")
		finally:
			Utils.sep()
	return links

def step3_download_zips(links):
	print("STEP 3: Downloading archives")
	Utils.sep()
	# create dir
	directory = 'downloaded'
	Utils.create_directory(directory)
	# download zips
	local_files = []
	for url in links:
		print(url)
		local_files.append(download_file(url, directory))
	return local_files

def step4_unzip(zip_files):
	print("STEP 4: Unzipping")
	Utils.sep()
	# create dir
	directory = 'downloaded/AddOns'
	Utils.create_directory(directory)
	# unzip
	for zipfile in zip_files:
		print("Extracting", zipfile)
		Utils.extract_zip('downloaded/' + zipfile, directory)


# main functions
step0_title()
addons = step1_scan()
links = step2_get_archives(addons)
local_files = step3_download_zips(links)
step4_unzip(local_files)
