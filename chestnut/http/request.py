from fir import http


class Request(http.Request):

	__slots__ = ["_json", "_files"]

	def __init__(self, *args, **kwargs):
		self._files = kwargs.pop("files", None)
		super().__init__(*args, **kwargs)
		self._json = None

	@property
	def json(self):
		if self._json is None:
			try:
				self._json = self.get_json()
			except:
				return {}
		return self._json

	@property
	def files(self):
		return self._files
