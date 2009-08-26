# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import gtk
import gtk.gdk
import gtk.glade
import gobject
from os.path import dirname, join

AFM_LOGO_PATH = join(dirname(__file__), 'data', 'afm.png')
AFM_LOGO_PIXBUF = gtk.gdk.pixbuf_new_from_file(AFM_LOGO_PATH)

if '_' not in __builtins__:
    def _(string):
        return string

class BaseGladeWidget(gobject.GObject):
    gladefile = None

    def __init__(self, app):
        if not self.gladefile:
            raise RuntimeError("You must define the 'gladefile' class attribute")
        self.__gobject_init__()
        self.app = app
        self.wTree = gtk.glade.XML(self.gladefile)
        self.wTree.signal_autoconnect(self.get_signal_handlers())
        self.prepare_widget()

    def get_signal_handlers(self):
        return {}

    def prepare_widget(self):
        pass
