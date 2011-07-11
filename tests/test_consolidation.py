# -*- coding: utf-8 -*-


import unittest
import sys; sys.path.append("../src")

from log_lines_manager import LogLinesManager
from exception import *


class TestConsolidation(unittest.TestCase):
    def testCountInitialization(self):
        conf = {'log_filename' : 'test.log',
                'events_conf' : [{'eventtype' : 'access',
                                  'regexps' : [],
                                  'consolidation_conf' : {'field' : 'accesses'}}, 
                                 {'eventtype' : 'user',
                                  'regexps' : [], 
                                  'consolidation_conf' : {'field' : 'users'}}]}
        log_manager = LogLinesManager(conf)
        expected_consolidated = {0 : {'eventtype': 'access', 'accesses' : 0},
                                 1 : {'eventtype': 'user', 'users' : 0}}
        consolidated = log_manager.consolidated
        self.assertDictEqual(expected_consolidated, consolidated)

    def testMatching(self):
        conf = {'log_filename' : 'test.log',
                'global_fields' : {'global-key' : 'global-value'},
                'events_conf' : [{'eventtype' : 'access',
                                  'regexps' : ['.*access.*'],
                                  'consolidation_conf' : {'field' : 'accesses'}}, 
                                 {'eventtype' : 'user',
                                  'regexps' : ['.*users.*'], 
                                  'consolidation_conf' : {'field' : 'users'}}]}
        log_manager = LogLinesManager(conf)
        log_manager.process_line('access test')
        log_manager.process_line('users test')
        expected_consolidated = {0 : {'eventtype': 'access', 'global-key' : 'global-value', 'accesses' : 1},
                                 1 : {'eventtype': 'user', 'global-key' : 'global-value', 'users' : 1}}
        consolidated = log_manager.consolidated
        self.assertDictEqual(expected_consolidated, consolidated)


    def testNoConsolidationConfs(self):
        conf = {'log_filename' : 'test.log',
                'events_conf' : [{'eventtype' : 'my-type', 'regexps' : []}]}
        log_manager = LogLinesManager(conf)
        expected_consolidated = {}
        consolidated = log_manager.consolidated
        self.assertDictEqual(expected_consolidated, consolidated)


if __name__ == "__main__":
    unittest.main()
