# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import gst
from afm.checks import BaseChecker

class SilenceChecker(BaseChecker):

    def __init__(self, min_tolerance=3000, max_tolerance=7000,
                 silence_level=-65):
        BaseChecker.__init__(self, min_tolerance=min_tolerance,
                             max_tolerance=max_tolerance)
        self.silence_level = silence_level

    def prepare_test(self):
        self.trigger_timeout = 1000 # 3 seconds
        # Level Check Element
        self.gst_element = self.gst_element_factory_make('level')
        self.gst_element.set_property('interval', 50000000)
        bus = self.source.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.check_bus_messages)

    def check_bus_messages(self, bus, message):
        if message.structure.get_name() == 'level':
#            print message.structure.to_string()
            rms_left, rms_right = message.structure['rms']
            if not self.trigger_active and not self.trigger_expired:
                if (rms_left or rms_right) < self.silence_level:
                    self.trigger()
            elif self.trigger_expired:
                if (rms_left and rms_right) < self.silence_level:
                    self.emit_failure("Audio failure on both channels")
                elif rms_left < self.silence_level:
                    self.emit_failure("Audio failure on left channel")
                elif rms_right < self.silence_level:
                    self.emit_failure("Audio failure on right channel")
                elif (rms_left or rms_right) > self.silence_level:
                    self.stop_trigger("Audio resumed")
            elif self.trigger_active and \
                                (rms_left or rms_right) > self.silence_level:
                self.kill_trigger()
        return True

