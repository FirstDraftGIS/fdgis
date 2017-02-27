#-*- coding: utf-8 -*-

from sys import version_info
python_version = version_info.major

import unittest
from fdgis import make_map

class TestStringMethods(unittest.TestCase):

    def testNJ(self):
        source = "He visited New Jersey last year."
        response = make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-74.49987, 40.16706])

    def testArlingtonTX(self):
        source = "He visited Arlington, TX"
        response = make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-97.10807, 32.73569])


    def testArlingtonVA(self):
        source = "He visited Arlington, VA"
        response = make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-77.10428, 38.88101])

    def testImages(self):
        source = "He visited Arlington, VA"
        image = make_map(source, map_format="png")
        image.save("/tmp/test.png")



if __name__ == '__main__':
    unittest.main()
