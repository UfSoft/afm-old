# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import gst
from urlparse import urlparse
from afm.sources import BaseAudioSource

class AudioFile(BaseAudioSource):

    def prepare_source(self):
        parsed_uri = urlparse(self.uri, 'file', allow_fragments=False)
        self.source = gst.element_factory_make("filesrc", "audiofile")
        self.source.set_property('location', parsed_uri.path)
#        print 123, self.source

    def link(self, link_to):
        return self.source.link(link_to)
