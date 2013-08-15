import sublime, sublime_plugin
from os.path import dirname, splitdrive, isfile, join, splitext
import os, sys
import thread
import subprocess
import functools
import time
import processlistener
import asynclistener

path = {
	'x32': "C:/Program Files/BYOND/bin/",
	'x64': "C:/Program Files (x86)/BYOND/bin/"
}

class ProcessListener(object):
    def on_data(self, proc, data):
        pass

    def on_finished(self, proc):
        pass

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

# Encapsulates subprocess.Popen, forwarding stdout to a supplied
# ProcessListener (on a separate thread)
class AsyncProcess(object):
    def __init__(self, arg_list, env, listener,
            # "path" is an option in build systems
            path="",
            # "shell" is an options in build systems
            shell=False):

        self.listener = listener
        self.killed = False

        self.start_time = time.time()

        # Hide the console window on Windows
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Set temporary PATH to locate executable in arg_list
        if path:
            old_path = os.environ["PATH"]
            # The user decides in the build system whether he wants to append $PATH
            # or tuck it at the front: "$PATH;C:\\new\\path", "C:\\new\\path;$PATH"
            os.environ["PATH"] = os.path.expandvars(path).encode(sys.getfilesystemencoding())

        proc_env = os.environ.copy()
        proc_env.update(env)
        for k, v in proc_env.iteritems():
            proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

        self.proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=shell)

        if path:
            os.environ["PATH"] = old_path

        if self.proc.stdout:
            thread.start_new_thread(self.read_stdout, ())

        if self.proc.stderr:
            thread.start_new_thread(self.read_stderr, ())

    def kill(self):
        if not self.killed:
            self.killed = True
            self.proc.terminate()
            self.listener = None

    def poll(self):
        return self.proc.poll() == None

    def exit_code(self):
        return self.proc.poll()

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2**15)

            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stdout.close()
                if self.listener:
                    self.listener.on_finished(self)
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2**15)

            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stderr.close()
                break
