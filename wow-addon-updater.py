# coding: utf-8

import wow_addons_toc

print("=================")
print("WoW Addon Updater")
print("-----------------")

tocs = wow_addons_toc.scan('AddOns')
print("Found %d directories" % len(tocs))
for toc in tocs:
    name = wow_addons_toc.find_name(toc)
    if name not in addons:
        version = wow_addons_toc.find_version(toc)
        is_curse = wow_addons_toc.is_curse(toc)
        print("Found %s (version: %s) %s" % (name, version, 'Curse' if is_curse else ''))