import re, requests, os, zipfile

class Utils:
	@staticmethod
	def run_regex_and_return_string(pattern, binary_data):
		regex = re.compile(pattern, re.I)
		match = regex.search(binary_data)
		if match:
			return str(match.group(1), encoding = 'UTF-8').strip()
		else:
			return None

	@staticmethod
	def sep(style = '-'):
		print(style * 30)

	@staticmethod
	def download_file(url, directory):
		local_filename = url.split('/')[-1]
		# NOTE the stream=True parameter
		r = requests.get(url, stream = True)
		with open(directory + '/' + local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size = 1024):
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()
		return local_filename

	@staticmethod
	def create_directory(directory):
		if not os.path.exists(directory):
			os.makedirs(directory)

	@staticmethod
	def extract_zip(zipfilepath, extractiondir):
		zip = zipfile.ZipFile(zipfilepath)
		zip.extractall(path = extractiondir)

	@staticmethod
	def unzip(source_filename, dest_dir):
		with zipfile.ZipFile(source_filename) as zf:
			for member in zf.infolist():
				# Path traversal defense copied from
				# http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
				words = member.filename.split('/')
				path = dest_dir
				for word in words[:-1]:
					drive, word = os.path.splitdrive(word)
					head, word = os.path.split(word)
					if word in (os.curdir, os.pardir, ''): continue
					path = os.path.join(path, word)
				zf.extract(member, path)
