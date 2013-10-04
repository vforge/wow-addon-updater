from .WowUtils import WowUtils

class WowAddonsRepository:
    """Abstract WoW Addons repository"""

    @staticmethod
    def factory(addon):
        for cls in WowAddonsRepository.__subclasses__():
            if cls.is_valid_for(addon):
                return cls
        raise ValueError

    @classmethod
    def is_valid_page(cls, addon):
        return WowUtils.are_we_online() and WowUtils.is_responding(cls.get_url_for(addon))


class WowRepositoryWowAce(WowAddonsRepository):
    def __init__(self):
        self.name = 'WowAce'

    @classmethod
    def is_valid_for(cls, addon):
        return addon.is_curse()

    @classmethod
    def get_url_for(cls, addon):
        return "http://www.wowace.com/addons/%s/" % addon.curse_project_id

class WowRepositoryCurseforge(WowAddonsRepository):
    def __init__(self):
        self.name = 'Curseforge'

    @classmethod
    def is_valid_for(cls, addon):
        return addon.is_curse()

    @classmethod
    def get_url_for(cls, addon):
        return "http://wow.curseforge.com/addons/%s/" % addon.curse_project_id


class WowRepositoryTukui(WowAddonsRepository):
    def __init__(self):
        self.name = 'TukUI'

    @classmethod
    def is_valid_for(cls, addon):
        return addon.is_tukui()
