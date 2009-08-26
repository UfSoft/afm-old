# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from xml.etree import cElementTree

class XMLSource(object):
    def __init__(self, filename):
        self.tree = cElementTree.parse(filename)
        self.source = self.tree.getroot()

    def get_uri(self):
        return self.source.get('uri')

    def get_tests(self):
        tests = self.source.find('tests')
        for test in tests.findall('test'):
            test_module = test.get('module')
            test_class = test.get('class')
            klass = __import__(test_module, fromlist=[test_class])
            yield klass(self.get_uri())
        raise StopIteration
