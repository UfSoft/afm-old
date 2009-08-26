# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import gtk
from os.path import dirname, join
from afm.gui.glade import BaseGladeWidget, AFM_LOGO_PATH

COLUMN_DATE, COLUMN_SOURCE, COLUMN_TYPE, COLUMN_MESSAGE = range(4)
class FailuresWindow(BaseGladeWidget):
    gladefile = join(dirname(__file__), 'data', 'glade', 'main_window.glade')

    def prepare_widget(self):
        self.window = self.wTree.get_widget('mainWindow')
        self.window.set_icon_from_file(AFM_LOGO_PATH)
        self.window.connect('delete_event', self.dont_destroy_window)
        self.failuresTreeView = self.wTree.get_widget('failuresTreeView')
        self.failuresModel = gtk.ListStore(str, str, str, str)
        self.failuresModelIter = self.failuresModel.get_iter_first()
        self.failuresTreeView.set_model(self.failuresModel)

        self.add_failure_column("Date", COLUMN_DATE)
        self.add_failure_column("Source", COLUMN_SOURCE)
        self.add_failure_column("Type", COLUMN_TYPE)
        self.add_failure_column("Message", COLUMN_MESSAGE, True)
#        print dir(self.app.tester)

        self.app.tester.connect_signal('audio-ok', self.audio_debug)
        self.app.tester.connect_signal('audio-warning', self.audio_debug)
        self.app.tester.connect_signal('audio-failure', self.audio_debug)
        self.app.tester.connect_signal('audio-debug', self.audio_debug)

    def dont_destroy_window(self, widget, event):
        self.window.hide_all()
        return True

    def show(self):
        self.window.show_all()

    def maximize(self):
        self.window.maximize()

    def toggle_window(self, widget):
        if self.window.get_property("visible"):
            self.window.hide_all()
        else:
            self.window.show_all()

    def add_failure_column(self, title, column_id, expand=False):
        renderer = gtk.CellRendererText()
        renderer.set_data("column", column_id)
        column = gtk.TreeViewColumn(title, renderer,
                                    text=column_id)
        column.set_resizable(True)
        column.set_sort_column_id(column_id)
        column.set_expand(expand)
        self.failuresTreeView.append_column(column)


    def audio_debug(self, checker, type, message, stamp):
        iter = self.failuresModel.append()
        self.failuresModel.set(iter,
                               COLUMN_DATE, stamp,
                               COLUMN_SOURCE, checker.__class__.__name__,
                               COLUMN_TYPE, type,
                               COLUMN_MESSAGE, message)
        print 9999, checker, type, message, stamp
