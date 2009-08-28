
import gst
import gobject
from afm.utils import SourceConfig
from twisted.internet import reactor

class BaseAudioSource(gobject.GObject):

    def __init__(self, application, configfile):
        self.__gobject_init__()
        self.app = application
        self.config = SourceConfig(self, configfile)
        self.name = self.config.name
        self.uri = self.config.uri
        self.pipeline = gst.Pipeline("%s-pipeline" % ''.join(self.name.split()))
        self.bus = self.pipeline.get_bus()

        self.source = gst.element_factory_make('uridecodebin')
        self.source.set_property('uri', self.uri)
        self.sourcecaps = gst.Caps()
        self.sourcecaps.append_structure(gst.Structure("audio/x-raw-float"))
        self.sourcecaps.append_structure(gst.Structure("audio/x-raw-int"))
        self.source.set_property("caps", self.sourcecaps)

        self.pipeline.add(self.source)
        self.source.connect("pad-added", self.on_pad_added)
        self.source.connect("no-more-pads", self.on_no_more_pads)
        self.pipeline.set_state(gst.STATE_PAUSED)
        self.source.set_state(gst.STATE_PAUSED)


    def connect_signal_to_tests(self, *args, **kwargs):
        for test in self.tests:
            test.connect(*args, **kwargs)

    def on_no_more_pads(self, dbin):
        reactor.callLater(0, self.pipeline.set_state, gst.STATE_PLAYING)

    def gst_element_factory_make(self, element_name):
        return gst.element_factory_make(
            element_name, '-'.join([element_name, ''.join(self.name.split())])
        )

    def on_pad_added(self, dbin, sink_pad):
        c = sink_pad.get_caps().to_string()
        if c.startswith("audio/"):
            self.convert = self.gst_element_factory_make('audioconvert')
            self.pipeline.add(self.convert)
            self.resample = self.gst_element_factory_make('audioresample')
            self.pipeline.add(self.resample)

            self.sink = self.gst_element_factory_make('alsasink')
            self.pipeline.add(self.sink)

            self.source.link(self.convert)
            self.convert.link(self.resample)

            # TESTS
            last_test = self.resample
            self.tests = []
            for test in self.config.get_tests():
                test.prepare_test()
                self.pipeline.add(test())
                self.tests.append(test)
                last_test.link(test())
                last_test = test()
                test().set_state(gst.STATE_PAUSED)
            last_test.link(self.sink)

            self.convert.set_state(gst.STATE_PAUSED)
            self.resample.set_state(gst.STATE_PAUSED)
            self.sink.set_state(gst.STATE_PAUSED)
            self.app.connect_signals()
        return True

    def __call__(self):
        return self.source

    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)
