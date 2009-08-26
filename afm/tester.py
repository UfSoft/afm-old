# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import afm
import gst
import gobject
from twisted.internet import reactor

class AudioTester(gobject.GObject):
    def __init__(self, app):
        self.__gobject_init__()
        self.app = app
        source_uri = 'file:///home/vampas/projects/AudioFailureMonitor/tests/FionaApple-FastAsYouCan2.wav'
        from afm.sources.audiofile import AudioFile


        self.pipeline = gst.Pipeline('audiotester')
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()

        self.src = AudioFile(source_uri)
        self.dec = gst.element_factory_make("decodebin2", "decodebin")

        # Connect handler for 'new-decoded-pad' signal
        self.dec.connect('new-decoded-pad', self.on_new_decoded_pad)
        self.conv = gst.element_factory_make('audioconvert')
        self.rsmpl = gst.element_factory_make('audioresample')
#        self.rsmpl = gst.element_factory_make('audioresample_f')
        self.sink = gst.element_factory_make('alsasink')

        # Add elements to pipeline
        self.pipeline.add(self.src(), self.dec, self.conv, self.rsmpl, self.sink)

        from afm.checks.silence import SilenceChecker
        s = SilenceChecker(self.pipeline)
        self.pipeline.add(s())
        tests = [s]

        # Link *some* elements
        # This is completed in self.on_new_decoded_pad()
        self.src.link(self.dec)
        gst.element_link_many(self.conv, self.rsmpl)

        testers = []
        last_tester = self.rsmpl
        for tester in tests:
            testers.append(tester)
            last_tester.link(tester())
            last_tester = tester()
        last_tester.link(self.sink)
        self.testers = testers


        # Reference used in self.on_new_decoded_pad()
        self.apad = self.conv.get_pad('sink')

#        reactor.callLater(5, tray.ErrorDialog, "Foo Bar!!!!")

    def connect_signal(self, *args, **kwargs):
        for tester in self.testers:
            tester.connect(*args, **kwargs)


    def on_new_decoded_pad(self, element, pad, last):
        caps = pad.get_caps()
        name = caps[0].get_name()
        print 'on_new_decoded_pad:', name
        if name == 'audio/x-raw-float' or name == 'audio/x-raw-int':
            if not self.apad.is_linked(): # Only link once
                pad.link(self.apad)

    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)
