import re, requests, Tools

class Utils:
	@staticmethod
	def current_interface_version():
		return 50400

	@staticmethod
	def remove_colors(string):
		if string is None:
			return None
		string = re.sub(r"\|\c........", "", string)
		return string.replace("|r", "")

	@staticmethod
	def find_in_toc(what, toc):
		return Tools.run_regex_and_return_string(bytes(what + ": (.*)\n", 'utf-8'), toc)

	@staticmethod
	def are_we_online():
		try:
			r = requests.get('http://google.com')
			if r.status_code == 200:
				return True
			else:
				return False
		finally:
			return False

