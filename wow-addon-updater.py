# coding: utf-8

import sys
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

# main functions
step0_title()
addons = step1_scan()
links = step2_get_archives(addons)

