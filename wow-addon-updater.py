# coding: utf-8

#imports
import glob
import codecs
import re

# defs
def scan_directory_for_toc(dir):
	tocs = glob.glob(dir + '/*/*.toc')
	print("Found %d directories" % len(tocs))
	return tocs
	
def run_regex_and_return_string(pattern, binary_data):
	regex = re.compile(pattern, re.I)
	match = regex.search(binary_data)
	if (match):
		return str(match.group(1), encoding='UTF-8').strip()
	else:
		return 0
	
def find_in_toc(string, toc_file):
	toc_data = open(toc_file, 'rb').read()
	return run_regex_and_return_string(bytes(string + ": (.*)\n", 'utf-8'), toc_data)
	

# find addon name from toc
def find_addon_name(toc_file):
	return find_in_toc("X-Curse-Project-Name", toc_file) or find_in_toc("Title", toc_file)

def find_addon_version(toc_file):
	return find_in_toc("X-Curse-Packaged-Version", toc_file) or find_in_toc("Version", toc_file)
	
# get addons list instead of tocs
def squish_tocs(tocs):
	addons = []
	for toc in tocs:
		name = find_addon_name(toc)
		if (name not in addons):
			version = find_addon_version(toc)
			print("Found %s (version: %s)" % (name, version))
			addons.append(name)
	return addons
	

# functions


## X-Curse-Packaged-Version: 6.2.6
## X-Curse-Project-Name: TellMeWhen
## X-Curse-Project-ID: tellmewhen
## X-Curse-Repository-ID: wow/tellmewhen/mainline

# Also dont forget to bump both of these - X-Interface is used to get the interface version in-game to check that the user is using a current client.
## Interface: 50400
# DONT FORGET TO TOC BUMP TELLMEWHEN_OPTIONS TOO!!
## X-Interface: 50400
## X-Compatible-With: 50400
## Title: TellMeWhen
## Version: 6.2.6

## X-Revision: $Rev: 318 $
## X-Curse-Packaged-Version: 2.45
## X-Curse-Project-Name: Skillet
## X-Curse-Project-ID: skillet

## Version: 1


# MAIN
print("=================")
print("WoW Addon Updater")
print("-----------------")

# find tocs
addon_tocs = scan_directory_for_toc('SampleAddOns')
addons = squish_tocs(addon_tocs)

