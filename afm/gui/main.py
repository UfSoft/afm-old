# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from afm import startup
import gobject
import gtk
from twisted.internet import reactor

from afm.checks import BaseChecker
from afm.gui.about import AboutDialog
from afm.gui.failures import FailuresWindow
from afm.gui.glade import AFM_LOGO_PATH, _
from afm.tester import AudioTester

class Application(gobject.GObject):
    def __init__(self):
        self.__gobject_init__()
        self.tester = AudioTester(self)
        reactor.callLater(1, self.tester.start)
        self.about_dialog = AboutDialog()
        self.tray_icon = self.create_tray_icon()
        self.menu = self.create_menu()
        self.failures = self.create_failures_window()
        self.failures.window.maximize()
        self.tray_icon.connect('activate', self.failures.toggle_window)

    def create_failures_window(self):
        return FailuresWindow(self)

    def create_tray_icon(self):
        """Creates and returns a tray icon for the application."""
        tray_icon = gtk.StatusIcon()
        tray_icon.set_from_file(AFM_LOGO_PATH)
        tray_icon.connect('popup-menu', self.popup_menu)
        tray_icon.set_tooltip('Audio Failure Monitor')
        tray_icon.set_visible(True)
        return tray_icon

    def create_menu(self):
        """Creates the menu obtained when right-clicking the tray icon."""
        about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        about.connect_object('activate', self.about, 'about')
        about.show()

#        prefs = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
#        prefs.connect_object('activate', self.prefs, 'prefs')
#        prefs.show()

        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect_object('activate', self.exit, 'quit')
        quit.show()

        menu = gtk.Menu()
        menu.append(about)
#        menu.append(prefs)
        menu.append(quit)
        return menu

    def popup_menu(self, status_icon, button, activate_time):
        """Handler to be called when the tray icon is right-clicked.

        Arguments:

            status_icon -- The tray icon object.
            button -- The button pressed.
            activate_time -- The time of the event.

        Shows the menu.
        """
        self.menu.popup(None, None, gtk.status_icon_position_menu, button,
                activate_time, status_icon)

    def about(self, widget):
        """Shows the about dialog."""
        self.about_dialog.show()

    def exit(self, widget):
        """Exits the application."""
        self.tray_icon.set_visible(False)
        self.tester.stop()
        reactor.stop()


if __name__ == '__main__':
    app = Application()
    reactor.run()
