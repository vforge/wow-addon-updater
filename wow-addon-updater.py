#!/usr/bin/env python
"""
SYNOPSIS
	wow-addons-updater [-h,--help] [-v,--verbose] [--version]

DESCRIPTION
	World of Warcraft AddOns updater - it tries to be smart :)

AUTHOR
	Bartosz V. Bentkowski

"""

import re, sys, os, traceback, argparse, time, Tools
from Wow.Addons import Addons
from Wow.AddonsRepository import AddonsRepository

def step0_title():
	Tools.sep("=")
	print("WoW Addon Updater")
	Tools.sep()


def step1_scan(directory):
	print("STEP 1: Scanning %s" % directory)
	Tools.sep()
	addons = Addons(directory)
	Tools.sep()
	return addons


def step2_get_archives(addons):
	counter, size, links = 0, len(addons.addons), []
	print("STEP 2: Finding archives")
	Tools.sep()
	for addon in addons.addons:
		counter += 1
		print("%d/%d: %s" % (counter, size, addon.name))
		try:
			repository = AddonsRepository.factory(addon)
			links.append(repository.get_downloading_link(addon))
		except ValueError:
			pass
	Tools.sep()
	return links


def step3_download_zips(links):
	print("STEP 3: Downloading %d archives" % len(links))
	Tools.sep()
	# create dir
	directory = 'downloaded'
	Tools.create_directory(directory)
	# download zips
	local_files = []
	for url in links:
		if url is None:
			print("Skipping empty url")
		else:
			print(url)
			local_files.append(Tools.download_file(url, directory))
	Tools.sep()
	return local_files


def step4_unzip(zip_files):
	global args

	print("STEP 4: Unzipping")
	Tools.sep()
	# create dir
	if args.debug:
		directory = 'downloaded/AddOns'
		Tools.create_directory(directory)
	else:
		directory = args.directory
	# unzip
	for zipfile in zip_files:
		print("Extracting", zipfile)
		Tools.extract_zip('downloaded/' + zipfile, directory)
	if not args.debug:
		Tools.sep()
		print('Removing "downloaded" directory')
		Tools.remove_directory('downloaded')
	Tools.sep()


def main():
	global args

	step0_title()
	addons = step1_scan(args.directory)
	links = step2_get_archives(addons)
	local_files = step3_download_zips(links)
	step4_unzip(local_files)


# RUN BLOCK
if __name__ == '__main__':
	try:
		start_time = time.time()
		parser = argparse.ArgumentParser(description = 'WoW AddOns Updater')

		parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = 'verbose output')
		parser.add_argument('-d', '--debug',   action = 'store_true', default = False, help = 'debug mode - DON\'T OVERRIDE ADDONS DIRECTORY CONTENTS')
		parser.add_argument('--dir', dest='directory', type=str, default='AddOnsSample', help='Directory to scan')

		args = parser.parse_args()
		if args.verbose:
			print('START:', time.asctime())
		main()
		if args.verbose:
			print('END:', time.asctime())
			print("TOTAL TIME IN MINUTES: %.2f" % ((time.time() - start_time) / 60.0))
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
	except SystemExit as e: # sys.exit()
		raise e
	except Exception as e:
		print('ERROR, UNEXPECTED EXCEPTION', str(e))
		traceback.print_exc()
		os._exit(1)
