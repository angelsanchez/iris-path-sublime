import sublime, sublime_plugin, json, re

class IrisPathCommand(sublime_plugin.EventListener):

	# Called when the file is finished loading
	def on_load(self, view):
		if self._is_iris_path(view):
			self._get_iris_path_items(view)
			sublime.status_message('iris-path.js file loaded')

	# Called after a view has been saved
	def on_post_save(self, view):
		if self._is_iris_path(view):
			self._get_iris_path_items(view)
			sublime.status_message('iris-path.js file refreshed')

	# Called when a view is closed
	def on_close(self, view):
		if self._is_iris_path(view):
			self.items = None
			sublime.status_message('iris-path.js file closed')

	# Called when user types in a view
	def on_query_completions(self, view, prefix, locations):
		
		# Skip if input text doesn't start with 'iris' or if current view is 'iris-path.js'
		if re.search('ir?i?s?', prefix) == None or self._is_iris_path(view):
			return
		
		if hasattr(self, 'items'):
			return self.items
		else:
			sublime.status_message('iris-path.js file not found!')


	def _is_iris_path(self, view):
		return view.file_name().endswith('iris-path.js')


	def _get_iris_path_items(self, view):
		
		iris_path_str = view.substr(sublime.Region(12, view.size()))
		iris_path_json = json.loads(iris_path_str)

		self.items = []
		self._add_json_to_items(iris_path_json, 'iris.path')

		sublime.status_message('iris.path loaded!')


	# Recursive
	def _add_json_to_items(self, prev_json, prev_path):
		for key in prev_json:
			json = prev_json[key]
			path = prev_path + '.' + key
			if type(json) is dict:
				self._add_json_to_items(json, path)
			else:
				# json is str
				self.items.append((path,path))
