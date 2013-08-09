import sublime_plugin, platform

path = {
	'32bit': "C:/Program Files/BYOND/bin",
	'64bit': "C:/Program Files (x86)/BYOND/bin"
}

class FindDMCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print platform.architecture()[0]
		print 'HAISDF'