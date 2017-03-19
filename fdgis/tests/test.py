#-*- coding: utf-8 -*-

from collections import Counter

from sys import version_info
python_version = version_info.major

import unittest
from fdgis import make_map

from os.path import dirname, realpath

path_to_directory_of_this_file = dirname(realpath(__file__))
print("path_to_directory_of_this_file:", dirname(realpath(__file__)))

class TestMethods(unittest.TestCase):

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

    def testDocx(self):
        with open(path_to_directory_of_this_file + "/test.docx", "rb") as f:
            geojson = make_map(f, map_format="geojson") 
            self.assertTrue(len(geojson['features']) >= 1)

    def testFormats(self):
        for _format in ["csv", "tsv", "xlsx"]:
            filepath = path_to_directory_of_this_file + "/test." + _format
            geojson = make_map(filepath) 
            self.assertEqual(len(geojson['features']), 7)

    def testTxt(self):
        filepath = path_to_directory_of_this_file + "/test.txt"
        geojson = make_map(filepath)
        self.assertEqual(len(geojson['features']), 1)

class TestLinks(unittest.TestCase):

    def testLinkTxt(self):
        geojson = make_map("https://raw.githubusercontent.com/FirstDraftGIS/fdgis/master/fdgis/tests/test.txt")
        self.assertEqual(len(geojson['features']), 1)

    def testPDFLink(self):
        source = "https://www.state.gov/documents/organization/253169.pdf"
        geojson = make_map(source, map_format="json")

    def testStructuredLinks(self):
        for extension in ["csv", "tsv", "xlsx"]:
            try:
                url = "https://raw.githubusercontent.com/FirstDraftGIS/fdgis/master/fdgis/tests/test." + extension
                geojson = make_map(url)
                self.assertEqual(len(geojson['features']), 7)
            except Exception as e:
                print("caught exception testing url: " + url)
                print(e)
                raise e


class Timeout(unittest.TestCase):

    def testTimeout(self):
        try:
            geojson = make_map("asdifhauwehf", timeout=1, timeout_raises_exception=True)
        except Exception as e:
            self.assertEqual(str(e), "Timeout")

        geojson = make_map("asdifhauwehf", timeout=1)
        self.assertEqual(geojson, None)

# commenting out until basemaps hit production
"""
class Basemap(unittest.TestCase):

    def testBasemap(self):
        image = make_map("South Africa, Hawaii", basemap="Stamen.Watercolor", map_format="image")
        # make sure colors match predominant basemap colors
        colors = [color for color, count Counter(image.getdata()).most_common(3)]
        self.assertTrue((251, 243, 232, 255) in colors)
        self.assertTrue((250, 242, 231, 255) in colors)
        self.assertTrue((249, 241, 230, 255) in colors)
"""

if __name__ == '__main__':
    unittest.main()
