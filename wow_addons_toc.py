import re
import glob
from progressBar import progressBar

def scan(dir):
    tocs = glob.glob(dir + '/*/*.toc')
    return tocs

def run_regex_and_return_string(pattern, binary_data):
    regex = re.compile(pattern, re.I)
    match = regex.search(binary_data)
    if match:
        return str(match.group(1), encoding='UTF-8').strip()
    else:
        return 0

def find(string, toc_file):
    toc_data = open(toc_file, 'rb').read()
    return run_regex_and_return_string(bytes(string + ": (.*)\n", 'utf-8'), toc_data)


# find addon name from toc
def find_name(toc_file):
    return find("X-Curse-Project-Name", toc_file) or find("Title", toc_file)

def find_version(toc_file):
    return find("X-Curse-Packaged-Version", toc_file) or find("Version", toc_file)

def is_curse(toc_file):
    return find("X-Curse-Project-Name", toc_file) != 0




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