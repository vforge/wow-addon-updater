import requests
import re
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

	def get_url_for(self, addon):
		return "http://www.wowace.com/addons/%s/" % addon.curse_project_id

	def get_full_url(self, partial_url):
		if partial_url[0:4] == 'http':
			return partial_url
		else:
			return "http://www.wowace.com%s" % partial_url

	@classmethod
	def get_downloading_link(cls, addon):
		url = cls.get_url_for(cls, addon)
		return cls.__download_chain(cls, url)

	def __download_chain(self, url):
		page = requests.get(url).content
		regex = re.compile(bytes('user-action-download">.*href="(.*)">Download', 'utf-8'), re.I|re.DOTALL)
		match = regex.search(page)
		if match:
			full_url = self.get_full_url(self, str(match.group(1), encoding='UTF-8').strip())
			print("Found match at: %s" % full_url)
			if full_url[-4:] == '.zip':
				return full_url
			else:
				return self.__download_chain(self, full_url)
		else:
			return None


class WowRepositoryCurseforge(WowAddonsRepository):
	def __init__(self):
		self.name = 'Curseforge'

	@classmethod
	def is_valid_for(cls, addon):
		return addon.is_curse()

	def get_url_for(self, addon):
		return "http://wow.curseforge.com/addons/%s/" % addon.curse_project_id

	def get_full_url(self, partial_url):
		if partial_url[0:4] == 'http':
			return partial_url
		else:
			return "http://wow.curseforge.com%s" % partial_url

	@classmethod
	def get_downloading_link(cls, addon):
		url = cls.get_url_for(cls, addon)
		return cls.__download_chain(cls, url)

	def __download_chain(self, url):
		page = requests.get(url).content
		regex = re.compile(bytes('user-action-download">.*href="(.*)">Download', 'utf-8'), re.I|re.DOTALL)
		match = regex.search(page)
		if match:
			full_url = self.get_full_url(self, str(match.group(1), encoding='UTF-8').strip())
			print("Found match at: %s" % full_url)
			if full_url[-4:] == '.zip':
				return full_url
			else:
				return self.__download_chain(self, full_url)
		else:
			return None


class WowRepositoryTukui(WowAddonsRepository):
	def __init__(self):
		self.name = 'TukUI'

	@classmethod
	def is_valid_for(cls, addon):
		return addon.is_tukui()

	def get_auto_download_url(self, addon):
		return "http://www.tukui.org/addons/index.php?act=download&id=%s" % addon.tukui_projectid

	@classmethod
	def get_downloading_link(cls, addon):
		url = cls.get_url_for(cls, addon)
		return cls.__download_chain(cls, url)
