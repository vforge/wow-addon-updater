import re

class WowUtils:
    @staticmethod
    def current_interface_version():
        return 50400

    @staticmethod
    def run_regex_and_return_string(pattern, binary_data):
        regex = re.compile(pattern, re.I)
        match = regex.search(binary_data)
        if match:
            return str(match.group(1), encoding='UTF-8').strip()
        else:
            return None

    @staticmethod
    def get_base_url_for_wowace(addon_name):
        return "http://www.wowace.com/addons/%s/" % addon_name

    @staticmethod
    def get_base_url_for_curseforge(addon_name):
        return "http://wow.curseforge.com/addons/%s/" % addon_name

    @staticmethod
    def remove_colors(string):
        if string is None:
            return None
        string = re.sub(r"\|\c........", "", string)
        return string.replace("|r", "")

    @staticmethod
    def find_in_toc(what, toc):
        return WowUtils.run_regex_and_return_string(bytes(what + ": (.*)\n", 'utf-8'), toc)