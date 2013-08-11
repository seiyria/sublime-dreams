import sublime, sublime_plugin
from os.path import dirname, splitdrive, isfile, join, splitext
from os import listdir

path = {
	'x32': "C:/Program Files/BYOND/bin/",
	'x64': "C:/Program Files (x86)/BYOND/bin/"
}

class DmcCommand(sublime_plugin.WindowCommand):

	def run(self, cmd = [], file_regex = ""):
		dmpath = path[sublime.arch()]

		self.build(dmpath, cmd[0], file_regex)

	def build(self, environment_path, file, file_regex):

		new_cmd = [ environment_path + "dm.exe" , self.find_closest_dme(file) ]
		sublime.active_window().run_command('exec', cmd = new_cmd, file_regex = file_regex)

	def find_closest_dme(self, compile_file):
		current_dir = compile_file

		dme = compile_file

		while current_dir != self.drive_root(current_dir):

			current_dir = dirname(current_dir)

			file_list = [ 
				current_dir+"\\"+f.encode('ascii', 'ignore') 
					for f in listdir(current_dir) 
						if isfile(join(current_dir, f)) and splitext(f)[1] == u".dme" 
				]

			#TODO search for the DME containing the file

			if len(file_list) is not 0:
				dme = file_list[0]

		return dme.encode('ascii', 'ignore') 

	def drive_root(self, path):
		return splitdrive(path)[0]+"\\"

	def run_in_seeker():
		print 'asdf'

	def run_in_daemon():
		print 'sdf'