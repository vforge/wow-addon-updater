# coding: utf-8

#imports
import glob
import json
import codecs
import re

# defs
def scan_directory_for_toc(dir):
	tocs = glob.glob(dir + '/*/*.toc')
	print("Found %d directories" % len(tocs))
	return tocs
	
def run_regex_and_return_string(pattern, data):
	regex = re.compile(pattern, re.I)
	return str(regex.search(data).group(1), encoding='UTF-8')
	

# find addon name from toc
def find_addon_name(toc_file):
	file_contents = open(toc_file, 'rb').read()
	return run_regex_and_return_string(b"Title: (.*)\n", file_contents)
	
# get addons list instead of tocs
def squish_tocs(tocs):
	addons = []
	for toc in tocs:
		print("Opening : %s" % toc)
		name = find_addon_name(toc)
		if (name not in addons):
			print("Found new addon: %s" % name)
			addons.append(name)
	return addons
	

# functions

# for next version
# open file
# file_data = open(file_name).read()
# read json data
# data = json.load(file_data)


# MAIN
print("WoW Addon Updater")

# find tocs
addon_tocs = scan_directory_for_toc('SampleAddOns')
addons = squish_tocs(addon_tocs)

