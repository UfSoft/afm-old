
import gobject
import gst
from datetime import datetime, timedelta

class BaseChecker(gobject.GObject):
    trigger_timeout = 3000
    warn_timeout = 7000
    warning_emitted = failure_emitted = False

    _ts = _te = None
    gst_element = None

    __gsignals__ = {
        'audio-warning': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
                          (str, str, str)),
        'audio-failure': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
                          (str, str, str)),
        'audio-ok': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
                     (str, str, str)),
        'audio-debug': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
                        (str, str, str)),
    }

    def __init__(self):
        self.__gobject_init__()

    def __call__(self):
        return self.gst_element

    def trigger(self):
        msg = 'Triggered, Warn in %d seconds' % (self.trigger_timeout/1000)
        self._ts = datetime.utcnow()
        self._te = self._ts + timedelta(seconds=self.trigger_timeout/1000)
        self.emit('audio-warning', 'WARNING', msg, str(self._ts))

    @property
    def trigger_active(self):
        return self._te and self._te > datetime.utcnow() or False

    @property
    def trigger_expired(self):
        return self._te and self._te < datetime.utcnow() or False

    def emit_debug(self, message):
        self.emit('audio-debug', 'DEBUG', message, str(self._ts))

    def emit_warning(self, message):
        if not self.warning_emitted:
            self.warning_emitted = True
            self.emit('audio-warning', 'WARNING', message, str(self._ts))

    def emit_failure(self, message):
        if not self.failure_emitted:
            self.failure_emitted = True
            self.emit('audio-failure', 'FAILURE', message, str(self._ts))

    def emit_ok(self, message="Trigger Stopped"):
        self.emit('audio-ok', 'WARNING', message, str(self._ts))

    def stop_trigger(self):
        self.emit_ok()
        self._ts = self._te = None
        self.failure_emitted = self.warning_emitted = False

gobject.type_register(BaseChecker)
#gobject.signal_new('audio-warning', BaseChecker, gobject.SIGNAL_RUN_FIRST,
#                   gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, str, str, str))
#gobject.signal_new('audio-failure', BaseChecker, gobject.SIGNAL_RUN_FIRST,
#                   gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, str, str, str))
#gobject.signal_new('audio-ok', BaseChecker, gobject.SIGNAL_RUN_FIRST,
#                   gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, str, str, str))
#gobject.signal_new('audio-debug', BaseChecker, gobject.SIGNAL_RUN_FIRST,
#                   gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, str, str, str))
