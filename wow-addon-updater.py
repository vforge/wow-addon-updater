# coding: utf-8

import sys
from libs.WowAddons import WowAddons
from libs.WowAddonsRepository import WowAddonsRepository

print("=================")
print("WoW Addon Updater")
print("-----------------")

directory = 'AddOnsSample'

if len(sys.argv) > 1:
    directory = sys.argv[1]

print("SCANNING: %s" % directory)
print("-----------------")
addons = WowAddons(directory)
for addon in addons.addons:
    addon.print()
    if addon.can_find_source_url():
        print('Url:', addon.find_source_url())
    print("-----------------")
