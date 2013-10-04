import requests

from .WowUtils import WowUtils

class WowAddon:
    def __init__(self, toc_file):
        self.current_interface = 50400

        self.toc_file = toc_file
        self.toc_data = open(toc_file, 'rb').read()
        self.title = WowUtils.remove_colors(self.find_in_toc("Title"))
        self.version = self.find_in_toc("Version")
        self.author = self.find_in_toc("Author")
        self.interface = self.find_in_toc("Interface")

        self.curse_project_name = self.find_in_toc("X-Curse-Project-Name")
        self.curse_package_version = self.find_in_toc("X-Curse-Packaged-Version")
        self.curse_repository_id = self.find_in_toc("X-Curse-Repository-ID")
        self.curse_projectid = self.find_in_toc("X-Curse-Project-ID")

        self.tukui_projectid = self.find_in_toc("X-Tukui-ProjectID")

        self.name = WowUtils.remove_colors(self.curse_project_name or self.title or None)

    def is_curse(self):
        return self.curse_project_name != None

    def is_tukui(self):
        return self.tukui_projectid != None

    def is_outdated(self):
        return int(self.interface) < self.current_interface

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

    def can_find_source_url(self):
        return self.is_curse()

    def get_curseforge(self):
        return requests.get(WowUtils.get_base_url_for_curseforge(self.curse_projectid))

    def get_wowace(self):
        return requests.get(WowUtils.get_base_url_for_wowace(self.curse_projectid))

    def try_curseforge(self):
        r = self.get_curseforge()
        if r.status_code == 200:
            return r.url
        else:
            return None

    def try_wowace(self):
        r = self.get_wowace()
        if r.status_code == 200:
            return r.url
        else:
            return None

    def find_source_url(self):
        if self.is_curse():
            return self.try_curseforge() or self.try_wowace() or ''

        raise Exception("Can't get source url - don't know how")
