# coding: utf-8

import sys
from libs.WowAddonScanner import WowAddonScanner

print("=================")
print("WoW Addon Updater")
print("-----------------")

directory = 'AddOnsSample'

if len(sys.argv) > 1:
    directory = sys.argv[1]

print("SCANNING: %s" % directory)
print("-----------------")
for addon in WowAddonScanner.scan(directory):
    addon.print()
    if addon.can_find_source_url():
        print('Url:', addon.find_source_url())
    print("-----------------")
