import re
import glob
from progressBar import progressBar

class WowUtils:
    def run_regex_and_return_string(pattern, binary_data):
        regex = re.compile(pattern, re.I)
        match = regex.search(binary_data)
        if match:
            return str(match.group(1), encoding='UTF-8').strip()
        else:
            return None

    def get_base_url_for_wowace(addon_name):
        return "http://www.wowace.com/addons/%s/" % addon_name

    def get_base_url_for_curseforge(addon_name):
        return "http://wow.curseforge.com/addons/%s/" % addon_name

class WowAddon:
    def __init__(self, toc_file):
        self.current_interface = 50400

        self.toc_file = toc_file
        self.toc_data = open(toc_file, 'rb').read()
        self.title = self.remove_colors(self.find_in_toc("Title"))
        self.version = self.find_in_toc("Version")
        self.author = self.find_in_toc("Author")
        self.interface = self.find_in_toc("Interface")

        self.curse_project_name = self.find_in_toc("X-Curse-Project-Name")
        self.curse_package_version = self.find_in_toc("X-Curse-Packaged-Version")
        self.curse_repository_id = self.find_in_toc("X-Curse-Repository-ID")
        self.curse_projectid = self.find_in_toc("X-Curse-Project-ID")

        self.tukui_projectid = self.find_in_toc("X-Tukui-ProjectID")

        self.name = self.remove_colors(self.curse_project_name or self.title or None)

    def is_curse(self):
        return self.curse_project_name != None

    def is_tukui(self):
        return self.tukui_projectid != None

    def is_outdated(self):
        return int(self.interface) < self.current_interface

    def remove_colors(self, string):
        if string == None:
            return None
        string = re.sub(r"\|\c........", "", string)
        return string.replace("|r", "")

    def find_in_toc(self, what):
        return WowUtils.run_regex_and_return_string(bytes(what + ": (.*)\n", 'utf-8'), self.toc_data)

    def print(self):
        author = ("by %s" % self.author) if self.author else ''
        print(self.title, author)
        if self.version:
            print("Version: %s" % self.version)

        print("Interface:", self.interface, '!!OUTDATED!!' if self.is_outdated() else '')

        if self.is_curse():
            print("[curse] Project ID: %s" % self.curse_projectid)
            print("[curse] Package Version: %s" % self.curse_package_version)

        if self.is_tukui():
            print("[tukui] Project ID: %s" % self.tukui_projectid)

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