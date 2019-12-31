from .key import Key

class Window:
	def __init__(self, title = '', keys = [], f_json = None):
		if f_json is not None:
			self.title = f_json['title_contains'] if 'title_contains' in f_json else title
			self.keys  = [ Key(kidx, f_json=ky) for kidx, ky in enumerate(f_json['keys']) ] if 'keys' in f_json else keys
		else:
			self.title = title
			self.keys  = keys

	def __str__(self):
		return f' Title: {self.title}\n Keys: {len(self.keys)} \n{self.keys}'

	def __repr__(self):
		return self.__str__()
