# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from xml.etree import cElementTree
from twisted.python.reflect import namedAny

class SourceConfig(object):
    _name = _uri = None
    def __init__(self, source, filename):
        self.source = source
        self.tree = cElementTree.parse(filename)
        self.root = self.tree.getroot()

    @property
    def uri(self):
        if not self._uri:
            self._uri = self.root.get('uri')
        return self._uri

    @property
    def name(self):
        if not self._name:
            self._name = self.root.get('name')
        return self._name

    def get_tests(self):
        tests = self.root.find('tests')
        for test in tests.findall('test'):
            yield load_test(self.source, test)
        raise StopIteration


PARAM_TYPES = {
    None:    str,
    'str':   str,
    'int':   int,
    'bool':  bool,
    'float': float
}


class ConfigParam(object):
    def __init__(self, config):
        self.name = config.get('name')
        self.type = config.get('type')
        self.value = PARAM_TYPES[self.type](config.get('value'))

def load_test(source, xmlconfig):
    params = {}
    module_name = xmlconfig.get('module')
    class_name = xmlconfig.get('class')
    params_node = xmlconfig.find('params')
    for param_node in params_node.findall('param'):
        param = ConfigParam(param_node)
        params[param.name] = param.value
    klass = namedAny('.'.join([module_name, class_name]))
    klass.source = source
    return klass(**params)

