class WowAddonsRepository:
    """Abstract WoW Addons repository"""
    def __init__(self, addon):
        self.addon = addon

    @staticmethod
    def factory(addon):
        for cls in WowAddonsRepository.__subclasses__():
            if cls.is_valid_for(addon):
                return cls(addon)

        raise ValueError


class WowRepositoryWowAce(WowAddonsRepository):
    def __init__(self, addon):
        self.name = 'WowAce'

    @classmethod
    def is_valid_for(cls, addon):
        return addon == 'a'


class WowRepositoryCurseforge(WowAddonsRepository):
    def __init__(self, addon):
        self.name = 'Curseforge'

    @classmethod
    def is_valid_for(cls, addon):
        return addon == 'b'

