#!/usr/bin/env python
"""
SYNOPSIS
	wow-addons-updater [-h,--help] [-v,--verbose] [--version]

DESCRIPTION
	World of Warcraft AddOns updater - it tries to be smart :)

AUTHOR
	Bartosz V. Bentkowski

"""

import sys, os, traceback, argparse, time
from libs.WowAddons import WowAddons
from libs.Utils import Utils
from libs.WowAddonsRepository import WowAddonsRepository


def step0_title():
	Utils.sep("=")
	print("WoW Addon Updater")
	Utils.sep()


def step1_scan(directory):
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
			pass
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
		local_files.append(Utils.download_file(url, directory))
	Utils.sep()
	return local_files


def step4_unzip(zip_files):
	global args

	print("STEP 4: Unzipping")
	Utils.sep()
	# create dir
	if args.debug:
		directory = 'downloaded/AddOns'
		Utils.create_directory(directory)
	else:
		directory = args.directory
	# unzip
	for zipfile in zip_files:
		print("Extracting", zipfile)
		Utils.extract_zip('downloaded/' + zipfile, directory)
	if not args.debug:
		Utils.sep()
		print('Removing "downloaded" directory')
		Utils.remove_directory('downloaded')
	Utils.sep()


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
		#if len(args) < 1:
		#    parser.error ('missing argument')
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
