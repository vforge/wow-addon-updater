import glob
from .ProgressBar import ProgressBar
from .WowAddon import WowAddon


class WowAddonScanner:
    def scan(dir):
        # scan dir in search of files
        tocs = glob.glob(dir + '/*/*.toc')
        len_tocs = len(tocs)

        print("Scanning %d ToC files" % len_tocs)
        prog = ProgressBar(maxValue = len_tocs)

        addons = []
        addon_names = []
        for toc in tocs:
            addon = WowAddon(toc)

            if addon.name and (addon.name not in addon_names):
                addons.append(addon)
                addon_names.append(addon.name)

            prog.appendAmount(1)
            prog.draw()

        print("\nFound %d addons" % len(addons))

        return addons