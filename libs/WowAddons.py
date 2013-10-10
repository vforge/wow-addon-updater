import glob
from .ProgressBar import ProgressBar
from .WowAddon import WowAddon


class WowAddons:
	def __init__(self, directory):
		self.directory = directory
		self.addon_tocs = []
		self.addons = []
		self.__perform_scan()

	def __perform_scan(self):
		# scan dir in search of files
		self.addon_tocs = glob.glob(self.directory + '/*/*.toc')
		len_tocs = len(self.addon_tocs)

		print("Scanning %d ToC files" % len_tocs)
		prog = ProgressBar(maxValue = len_tocs)

		self.addons = []
		addon_names = []
		for toc in self.addon_tocs:
			addon = WowAddon(toc)

			if addon.name and (addon.name not in addon_names):
				self.addons.append(addon)
				addon_names.append(addon.name)

			prog.appendAmount(1)
			prog.draw()

		print("\nFound %d addons" % len(self.addons))

		return self.addons
