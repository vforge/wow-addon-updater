# coding: utf-8

import sys, zipfile, os, requests
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
	
def create_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	
def step3_download_zips(links):
	print("STEP 3: Downloading archives")
	sep()
	# create dir
	directory = 'downloaded'
	create_directory(directory)
	# download zips
	local_files = []
	for url in links:
		print(url)
		local_files.append(download_file(url, directory))
	return local_files

def extract(zipfilepath, extractiondir):
    zip = zipfile.ZipFile(zipfilepath)
    zip.extractall(path=extractiondir)
	
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)
			
def step4_unzip(zip_files):
	print("STEP 4: Unzipping")
	sep()
	# create dir
	directory = 'downloaded/AddOns'
	create_directory(directory)
	# unzip
	for zipfile in zip_files:
		print("Extracting", zipfile)
		extract('downloaded/' + zipfile, directory)
	


# main functions
step0_title()
addons = step1_scan()
links = step2_get_archives(addons)
local_files = step3_download_zips(links)
step4_unzip(local_files)
