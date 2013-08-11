import sublime, sublime_plugin
from os.path import dirname, splitdrive, isfile, join, splitext
from os import listdir

path = {
	'x32': "C:/Program Files/BYOND/bin/",
	'x64': "C:/Program Files (x86)/BYOND/bin/"
}

class DmcCommand(sublime_plugin.WindowCommand):

	def run(self, cmd = [], file_regex = "", kill_old = False, dream_seeker = False, dream_daemon = False):
		dmpath = path[sublime.arch()]

		dme_dir = self.build(dmpath, cmd[0], file_regex)
		dmb_dir = self.find_dmb(dme_dir)

		if dream_seeker:
			self.run_in_seeker(dmpath, dmb_dir)

		if dream_daemon:
			self.run_in_daemon(dmpath, dmb_dir)

	def build(self, environment_path, file, file_regex):

		dme_path = self.find_closest_dme(file)

		new_cmd = [ environment_path + "dm.exe" , dme_path ]
		args = {
			'cmd': new_cmd,
			'file_regex': file_regex,
			'working_dir': dirname(dme_path)
		}
		sublime.active_window().run_command("exec", args)

		return dirname(dme_path)

	def find_dmb(self, current_dir):

		#TODO match the current directory name/dme name
		dmb_list = [ 
			current_dir+"\\"+f.encode('ascii', 'ignore') 
				for f in listdir(current_dir) 
					if isfile(join(current_dir, f)) and splitext(f)[1] == u".dmb" 
			]

		if len(dmb_list) is not 0:
			return dmb_list[0]

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

	def run_in_seeker(self, environment_path, dmb):
		new_cmd = [ environment_path + "dreamseeker.exe" , dmb ]
		args = {
			'cmd': new_cmd
		}
		sublime.active_window().run_command("exec", args)

	def run_in_daemon(self, environment_path, dmb):
		new_cmd = [ environment_path + "dreamdaemon.exe" , dmb , "-trusted" ]
		args = {
			'cmd': new_cmd
		}
		sublime.active_window().run_command("exec", args)