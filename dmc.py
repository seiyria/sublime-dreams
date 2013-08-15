import sublime, sublime_plugin
from os.path import dirname, splitdrive, isfile, join, splitext
import os, sys
import thread
import subprocess
import functools
import time
import asynclistener
import processlistener

path = {
	'x32': "C:/Program Files/BYOND/bin/",
	'x64': "C:/Program Files (x86)/BYOND/bin/"
}

class DmcCommand(sublime_plugin.WindowCommand, ProcessListener):

	dream_daemon = None
	dream_seeker = None

	#DreamMaker
	proc 	     = None

	quiet 		 = False

	def run(self, cmd = [], file_regex = "", line_regex = "",
            encoding = "utf-8", env = {}, quiet = False, kill_old = False,
            dream_seeker = False, dream_daemon = False, **kwargs):

		file = cmd[0]
		dmpath = path[sublime.arch()]

		dme_file = self.find_closest_dme(file)
		dme_dir = dirname(dme_file)

		self.setup_sublime(file_regex, line_regex, dme_dir, encoding)

		# kill it to prevent RSC bullshit
		if self.dream_seeker and kill_old:
			self.dream_seeker.kill()

		self.build(dmpath, dme_file)
		dmb_dir = self.find_dmb(dme_dir)

		if dream_seeker:
			self.run_in_seeker(dmpath, dmb_dir)

		if dream_daemon:
			self.run_in_daemon(dmpath, dmb_dir)

	def run_cmd(self, cmd, is_daemon = False, is_seeker = False, is_maker = False, **kwargs):

		self.proc = None

		merged_env = {}
		if self.window.active_view():
		    user_env = self.window.active_view().settings().get('build_env')
		    if user_env:
		        merged_env.update(user_env)

		err_type = OSError
		if os.name == "nt":
		    err_type = WindowsError

		try:
			# I have a large dislike of writing it this way
			if is_maker:
				sublime.status_message("Building DMB...")
				self.proc = AsyncProcess(cmd, merged_env, self, **kwargs)

			if is_seeker:					
				sublime.status_message("Running in DreamSeeker...")
				self.dream_seeker = AsyncProcess(cmd, merged_env, self, **kwargs)

			if is_daemon:					
				sublime.status_message("Running in DreamDaemon...")
				self.dream_daemon = AsyncProcess(cmd, merged_env, self, **kwargs)

		except err_type as e:
		    self.append_data(None, str(e) + "\n")
		    self.append_data(None, "[cmd:  " + str(cmd) + "]\n")
		    self.append_data(None, "[dir:  " + str(os.getcwdu()) + "]\n")
		    if "PATH" in merged_env:
		        self.append_data(None, "[path: " + str(merged_env["PATH"]) + "]\n")
		    else:
		        self.append_data(None, "[path: " + str(os.environ["PATH"]) + "]\n")
		    if not self.quiet:
		        self.append_data(None, "[Finished]")

#build runners

	def build(self, environment_path, dme_path):
		cmd = [ environment_path + "dm" , dme_path ]
		self.run_cmd(cmd, is_maker = True)

	def run_in_seeker(self, environment_path, dmb = ''):
		cmd = [ environment_path + "dreamseeker" , dmb ]
		self.run_cmd(cmd, is_seeker = True)

	def run_in_daemon(self, environment_path, dmb):
		cmd = [ environment_path + "dreamdaemon" , dmb , "-trusted" ]
		self.run_cmd(cmd, is_daemon = True)

#file finders

	def find_closest_dme(self, compile_file):
		sublime.status_message("Finding closest DME...")
		current_dir = compile_file

		dme = compile_file

		while current_dir != self.drive_root(current_dir):

			current_dir = dirname(current_dir)

			file_list = [ 
				current_dir+"\\"+f.encode('ascii', 'ignore') 
					for f in os.listdir(current_dir) 
						if isfile(join(current_dir, f)) and splitext(f)[1] == u".dme" 
				]

			#TODO search for the DME containing the file

			if len(file_list) is not 0:
				dme = file_list[0]

		return dme.encode('ascii', 'ignore') 


	def find_dmb(self, current_dir):
		#TODO match the current directory name/dme name
		dmb_list = [ 
			current_dir+"\\"+f.encode('ascii', 'ignore') 
				for f in os.listdir(current_dir) 
					if isfile(join(current_dir, f)) and splitext(f)[1] == u".dmb" 
			]

		if len(dmb_list) is not 0:
			return dmb_list[0]

#get the drive root

	def drive_root(self, path):
		return splitdrive(path)[0]+"\\"

#sublime configuration

	def setup_sublime(self, file_regex, line_regex, working_dir, encoding):
		if not hasattr(self, 'output_view'):
		    self.output_view = self.window.get_output_panel("exec")

		if (working_dir == "" and self.window.active_view()
		                and self.window.active_view().file_name()):
		    working_dir = os.path.dirname(self.window.active_view().file_name())

		self.output_view.settings().set("result_file_regex", file_regex)
		self.output_view.settings().set("result_line_regex", line_regex)
		self.output_view.settings().set("result_base_dir", working_dir)

		self.window.get_output_panel("exec")

		self.encoding = encoding

		show_panel_on_build = sublime.load_settings("Preferences.sublime-settings").get("show_panel_on_build", True)
		if show_panel_on_build:
		    self.window.run_command("show_panel", {"panel": "output.exec"})

		if working_dir != "":
		    os.chdir(working_dir)

# from exec.py verbatim

	def is_enabled(self, kill = False):
		if kill:
			return hasattr(self, 'proc') and self.proc and self.proc.poll()
		else:
			return True

	def append_data(self, proc, data):
		if proc != self.proc:
			# a second call to exec has been made before the first one
			# finished, ignore it instead of intermingling the output.
			if proc:
				proc.kill()
			return

		try:
			str = data.decode(self.encoding)
		except:
			str = "[Decode error - output not " + self.encoding + "]\n"
			proc = None

		# Normalize newlines, Sublime Text always uses a single \n separator
		# in memory.
		str = str.replace('\r\n', '\n').replace('\r', '\n')

		selection_was_at_end = (len(self.output_view.sel()) == 1
			and self.output_view.sel()[0]
			== sublime.Region(self.output_view.size()))

		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.insert(edit, self.output_view.size(), str)

		if selection_was_at_end:
			self.output_view.show(self.output_view.size())
			self.output_view.end_edit(edit)
			self.output_view.set_read_only(True)

	def finish(self, proc):
		if not self.quiet:
			elapsed = time.time() - proc.start_time
			exit_code = proc.exit_code()
			if exit_code == 0 or exit_code == None:
				self.append_data(proc, ("[Finished in %.1fs]") % (elapsed))
			else:
				self.append_data(proc, ("[Finished in %.1fs with exit code %d]") % (elapsed, exit_code))

		if proc != self.proc:
			return

		errs = self.output_view.find_all_results()
		if len(errs) == 0:
			sublime.status_message("Build finished")
		else:
			sublime.status_message(("Build finished with %d errors") % len(errs))

		# Set the selection to the start, so that next_result will work as expected
		edit = self.output_view.begin_edit()
		self.output_view.sel().clear()
		self.output_view.sel().add(sublime.Region(0))
		self.output_view.end_edit(edit)

	def on_data(self, proc, data):
		sublime.set_timeout(functools.partial(self.append_data, proc, data), 0)

	def on_finished(self, proc):
		sublime.set_timeout(functools.partial(self.finish, proc), 0)