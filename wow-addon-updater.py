# coding: utf-8

import sys
from libs.WowAddons import WowAddons
from libs.WowUtils import WowUtils
from libs.WowAddonsRepository import WowAddonsRepository

def title():
    print("=================")
    print("WoW Addon Updater")
    print("-----------------")

def scan():
    directory = 'AddOnsSample'

    if len(sys.argv) > 1:
        directory = sys.argv[1]

    print("SCANNING: %s" % directory)
    print("-----------------")

    return WowAddons(directory)

# main functions
title()
addons = scan()
counter, size = 0, len(addons.addons)

for addon in addons.addons:
    counter += 1
    print("%d/%d: %s" % (counter, size, addon.name))
