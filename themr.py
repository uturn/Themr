import sublime, sublime_plugin
import os
import json

themr = os.getcwd()

if sublime.version() <= 2174:
	pref = 'Preferences.sublime-settings'
else:
	pref = 'Global.sublime-settings'

def theme_data():
	settings = sublime.load_settings(pref)
	packages = os.listdir(sublime.packages_path())
	ignored_packages = settings.get('ignored_packages')
	themes = []
	data = []

	for package in (package for package in packages if package.startswith('Theme -') and package not in ignored_packages):
		theme = os.listdir(os.path.join(sublime.packages_path(), package))

		for filename in (filenames for filenames in theme if filenames.endswith('.sublime-theme')):
			themes.append(filename)

	sublime.status_message('Themr: ' + str(len(themes)) + ' theme(s) found.')

	for theme in themes:
		data.append({'caption': 'Themr: ' + os.path.splitext(theme)[0], 'command': 'switch_theme', 'args': { 't': theme }})

	data.append({'caption': 'Themr: Reload themes', 'command': 'reload_themes'})
	commands = json.dumps(data, indent = 4)

	f = open(os.path.join(sublime.packages_path(), themr, 'Default.sublime-commands'), 'w')
	f.write(commands + '\n')
	f.close

class SwitchThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		sublime.set_timeout(theme_data, 3000)

	def run(self, t):
		self.settings = sublime.load_settings(pref)
		
		if self.get_theme() != t:
			self.set_theme(t)

	def get_theme(self):
		return self.settings.get('theme', 'Default.sublime-theme')

	def set_theme(self, t):
		self.settings.set('theme', t)
		sublime.save_settings(pref)

		if self.get_theme() == t:
			sublime.status_message('Themr: ' + t)
		else:
			sublime.status_message('Error saving theme. The read/write operation may have failed.')

class ReloadThemesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		theme_data()
