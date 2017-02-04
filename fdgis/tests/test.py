#-*- coding: utf-8 -*-

from sys import version_info
python_version = version_info.major

import unittest
from fdgis import make_map

class TestStringMethods(unittest.TestCase):

    def test1(self):
        source = "He visited New Jersey last year."
        response = make_map(source)
        print 'response:', response


if __name__ == '__main__':
    unittest.main()
