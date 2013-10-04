import re

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

    def remove_colors(string):
        if string == None:
            return None
        string = re.sub(r"\|\c........", "", string)
        return string.replace("|r", "")