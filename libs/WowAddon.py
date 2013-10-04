import requests

from .WowUtils import WowUtils

class WowAddon:
    def __init__(self, toc_file):
        self.toc_file = toc_file
        self.toc_data = open(toc_file, 'rb').read()
        self.title = WowUtils.remove_colors(self.__find_in_toc("Title"))
        self.version = self.__find_in_toc("Version")
        self.author = self.__find_in_toc("Author")
        self.interface = self.__find_in_toc("Interface")

        self.curse_project_name = self.__find_in_toc("X-Curse-Project-Name")
        self.curse_package_version = self.__find_in_toc("X-Curse-Packaged-Version")
        self.curse_repository_id = self.__find_in_toc("X-Curse-Repository-ID")
        self.curse_project_id = self.__find_in_toc("X-Curse-Project-ID")

        self.tukui_projectid = self.__find_in_toc("X-Tukui-ProjectID")

        self.name = self.curse_project_name or self.title or None

    # boolean is_xxxx?
    def is_curse(self):
        return self.curse_project_name is not None

    def is_tukui(self):
        return self.tukui_projectid is not None

    def is_outdated(self):
        return int(self.interface) < WowUtils.current_interface_version()

    # private
    def __find_in_toc(self, what):
        return WowUtils.find_in_toc(what, self.toc_data)

    # to str :P
    def print(self):
        author = ("by %s" % self.author) if self.author else ''
        print(self.title, author)
        if self.version:
            print("Version: %s" % self.version)

        print("Interface:", self.interface, '!!OUTDATED!!' if self.is_outdated() else '')

        if self.is_curse():
            print("[curse] Project ID: %s" % self.curse_project_id)
            print("[curse] Package Version: %s" % self.curse_package_version)

        if self.is_tukui():
            print("[tukui] Project ID: %s" % self.tukui_projectid)
    #
    #def try_curseforge(self):
    #    r = self.get_curseforge()
    #    if r.status_code == 200:
    #        return r.url
    #    else:
    #        return None
    #
    #def try_wowace(self):
    #    r = self.get_wowace()
    #    if r.status_code == 200:
    #        return r.url
    #    else:
    #        return None
    #
    #def find_source_url(self):
    #    if self.is_curse():
    #        return self.try_curseforge() or self.try_wowace() or ''
    #
    #    raise Exception("Can't get source url - don't know how")
