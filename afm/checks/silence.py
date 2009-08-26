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


    def __init__(self, pipeline, silence_level=-65):
        BaseChecker.__init__(self)
        self.silence_level = silence_level
        self.trigger_timeout = 1000 # 3 seconds
        # Level Check Element
        self.gst_element = gst.element_factory_make('level', 'silence_checker')
        self.gst_element.set_property('interval', 50000000)
        bus = pipeline.get_bus()
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
                if rms_left < self.silence_level:
                    self.emit_failure("Audio failure on left channel")
                elif rms_right < self.silence_level:
                    self.emit_failure("Audio failure on right channel")
                elif (rms_left and rms_right) < self.silence_level:
                    self.emit_failure("Audio failure on both channels")
                elif (rms_left or rms_right) > self.silence_level:
                    self.stop_trigger()
            elif self.trigger_active and \
                                (rms_left or rms_right) > self.silence_level:
                self.stop_trigger()
        return True

