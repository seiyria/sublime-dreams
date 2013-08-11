import sublime, sublime_plugin

path = {
	'X32': "C:/Program Files/BYOND/bin",
	'X64': "C:/Program Files (x86)/BYOND/bin"
}

class DmcCommand(sublime_plugin.WindowCommand):
	def run(self, cmd = [], file_regex = "", line_regex = "", **kwargs):
		self.view.error_message("ASDF")
		self.view.error_message(self.view.platform())

	def find_dm():
		self.view.error_message("findign dm!")