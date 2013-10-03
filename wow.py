import re
import glob
from progressBar import progressBar

def run_regex_and_return_string(pattern, binary_data):
    regex = re.compile(pattern, re.I)
    match = regex.search(binary_data)
    if match:
        return str(match.group(1), encoding='UTF-8').strip()
    else:
        return None


class WowAddon:
    def __init__(self, toc_file):
        self.toc_file = toc_file
        self.toc_data = open(toc_file, 'rb').read()
        self.title = self.find_in_toc("Title")
        self.version = self.find_in_toc("Version")
        self.author = self.find_in_toc("Author")
        self.curse_project_name = self.find_in_toc("X-Curse-Project-Name")
        self.curse_package_version = self.find_in_toc("X-Curse-Packaged-Version")
        self.name = self.curse_project_name or self.title or None
        self.full_version = self.curse_package_version or self.version or None

    def find_in_toc(self, what):
        return run_regex_and_return_string(bytes(what + ": (.*)\n", 'utf-8'), self.toc_data)

    def print(self):
        version = ("(v. %s)" % self.full_version) if self.full_version else ''
        author = ("by %s" % self.author) if self.author else ''
        print(self.name, version, author)

class WowAddonScanner:
    def scan(dir):
        # scan dir in search of files
        tocs = glob.glob(dir + '/*/*.toc')
        len_tocs = len(tocs)

        print("Scanning %d ToC files" % len_tocs)
        prog = progressBar(maxValue = len_tocs)

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