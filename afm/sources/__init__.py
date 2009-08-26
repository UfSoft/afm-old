

class BaseAudioSource(object):
    source = None

    def __init__(self, uri):
        self.uri = uri
        self.prepare_source()

    def __call__(self):
        return self.source

    def prepare_source(self):
        raise NotImplementedError("prepare_source() must be overridden by your "
                                  "subclass.")
