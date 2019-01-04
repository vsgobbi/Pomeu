# Interface script for GTK window
# Modified Vitor Sgobbi, 2014
# ICEA (Air traffic control insitute) - Brazil
# This code is licensed GPL
import sys
import gobject

import pygtk
import gtk

class UI(gobject.GObject):
	__gsignals__ = {
		'command' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
	}

	def __init__(self,args, continuous):
		gobject.GObject.__init__(self)
		self.continuous = continuous

		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_title("Pomeu")
		self.statusicon.set_name("Pomeu")
		self.statusicon.set_tooltip_text("Pomeu - Idle")
		self.statusicon.set_has_tooltip(True)
		self.statusicon.connect("activate", self.continuous_toggle)
		self.statusicon.connect("popup-menu", self.popup_menu)

		self.menu = gtk.Menu()
		self.menu_listen = gtk.MenuItem('Listen')
		self.menu_continuous = gtk.CheckMenuItem('Continuous')
		self.menu_quit = gtk.MenuItem('Quit')
		self.menu.append(self.menu_listen)
		self.menu.append(self.menu_continuous)
		self.menu.append(self.menu_quit)
		self.menu_listen.connect("activate", self.toggle_listen)
		self.menu_continuous.connect("toggled", self.toggle_continuous)
		self.menu_quit.connect("activate", self.quit)
		self.menu.show_all()

	def continuous_toggle(self, item):
		checked = self.menu_continuous.get_active()
		self.menu_continuous.set_active(not checked)

	def toggle_continuous(self, item):
		checked = self.menu_continuous.get_active()
		self.menu_listen.set_sensitive(not checked)
		if checked:
			self.menu_listen.set_label("Listen")
			self.emit('command', "escutar continuo")
			self.statusicon.set_tooltip_text("Pomeu - Listening")
			self.set_icon_active()
		else:
			self.set_icon_inactive()
			self.statusicon.set_tooltip_text("Pomeu - Idle")
			self.emit('command', "parado")

	def toggle_listen(self, item):
		val = self.menu_listen.get_label()
		if val == "Listen":
			self.emit("command", "listen")
			self.menu_listen.set_label("Stop")
			self.statusicon.set_tooltip_text("Pomeu - Listening")
		else:
			self.icon_inactive()
			self.menu_listen.set_label("Listen")
			self.emit("command", "stop")
			self.statusicon.set_tooltip_text("Pomeu - Idle")

	def popup_menu(self, item, button, time):
		self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, item)

	def run(self):
		#set the icon
		self.set_icon_inactive()
		if self.continuous:
			self.menu_continuous.set_active(True)
			self.set_icon_active()
		else:
			self.menu_continuous.set_active(False)
		self.statusicon.set_visible(True)

	def quit(self, item):
		self.statusicon.set_visible(False)
		self.emit("command", "quit")

	def finished(self, text):
		print text
		if not self.menu_continuous.get_active():
			self.menu_listen.set_label("Listen")
			self.statusicon.set_from_icon_name("pomeu_stopped")
			self.statusicon.set_tooltip_text("Pomeu - Idle")

	def set_icon_active_asset(self, i):
		self.icon_active = i

	def set_icon_inactive_asset(self, i):
		self.icon_inactive = i

	def set_icon_active(self):
		self.statusicon.set_from_file( self.icon_active )

	def set_icon_inactive(self):
		self.statusicon.set_from_file( self.icon_inactive )

