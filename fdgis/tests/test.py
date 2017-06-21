#-*- coding: utf-8 -*-

from collections import Counter

from sys import version_info
python_version = version_info.major

import unittest
import fdgis

from os import listdir
from os.path import dirname, join, realpath
#from tempfile import gettempdir
from tempfile import mkdtemp

path_to_directory_of_this_file = dirname(realpath(__file__))
print("path_to_directory_of_this_file:", dirname(realpath(__file__)))

fdgis.default_url_to_server = "https://dev.firstdraftgis.com"

class TestTimezone(unittest.TestCase):

    def testClarendon(self):
        source = "I like Clarendon"
        geojson = fdgis.make_map(source, debug=True, end_user_timezone="America/New_York")
        self.assertEqual(geojson['features'][0]['properties']['timezone'], "America/New_York")

class TestShapefile(unittest.TestCase):
    def testShp1(self):
        source = "Where is Richmond, VA?"
        zipped_shapefile = fdgis.make_map(source, map_format="shapefile", debug=True)
        try:
            from django.contrib.gis.gdal import DataSource
        except:
            DataSource = None
        if DataSource:
            path_to_tmp_dir = mkdtemp()
            zipped_shapefile.extractall(path_to_tmp_dir)
            for filename in listdir(path_to_tmp_dir):
                if filename.endswith(".shp"):
                    ds = DataSource(join(path_to_tmp_dir, filename))
                    self.assertEqual(ds.layer_count, 1)
                    self.assertEqual(list(list(ds)[0])[0].get("name"), "Richmond")

class TestMethods(unittest.TestCase):

    def testAleppo(self):
        source = "Where is Aleppo, Syria?"
        response = fdgis.make_map(source, debug=False)
        #self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-74.49987, 40.16706])
        self.assertEqual(response['features'][0]['properties']['name'], "Aleppo")
        self.assertEqual(response['features'][0]['properties']['country_code'], "SY")
        self.assertEqual(len(response['features']), 1)

    def testParisUnitedState(self):
        source = "Where is Paris, United States?"
        response = fdgis.make_map(source, debug=False)
        self.assertEqual(response['features'][0]['properties']['name'], "Paris")
        self.assertEqual(response['features'][0]['properties']['country_code'], "US")

    def testParisTexas(self):
        source = "Where is Paris, Texas?"
        response = fdgis.make_map(source, debug=True)
        self.assertEqual(response['features'][0]['properties']['name'], "Paris")
        self.assertEqual(response['features'][0]['properties']['country_code'], "US")
        self.assertEqual(response['features'][0]['properties']['admin1code'], "TX")
 
         

    def testNonAscii(self):
        source = "Despite a promise not to campaign following the attack Thursday night on Parisâs renowned Champs-ÃlysÃ©es boulevard, far-right candidate Marine Le Pen reinforced her anti-immigrant message in a Friday speech, calling on the French government to immediately reinstate border checks and expel foreigners being monitored by the intelligence services."
        response = fdgis.make_map(source, debug=True)
        print("response:" + str(response))

    def testNJ(self):
        source = "He visited New Jersey last year."
        response = fdgis.make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-74.49987, 40.16706])

    def testArlingtonTX(self):
        source = "He visited Arlington, TX"
        response = fdgis.make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-97.10807, 32.73569])


    def testArlingtonVA(self):
        source = "He visited Arlington, VA"
        response = fdgis.make_map(source)
        self.assertEqual(response['features'][0]['geometry']['geometries'][0]['coordinates'], [-77.10428, 38.88101])

    def testImages(self):
        source = "He visited Arlington, VA"
        image = fdgis.make_map(source, map_format="png")
        image.save("/tmp/test.png")

    def testDocx(self):
        with open(path_to_directory_of_this_file + "/test.docx", "rb") as f:
            geojson = fdgis.make_map(f, map_format="geojson") 
            self.assertTrue(len(geojson['features']) >= 1)

    def testFormats(self):
        for _format in ["csv", "tsv", "xlsx"]:
            filepath = path_to_directory_of_this_file + "/test." + _format
            geojson = fdgis.make_map(filepath) 
            self.assertEqual(len(geojson['features']), 7)

    def testTxt(self):
        filepath = path_to_directory_of_this_file + "/test.txt"
        geojson = fdgis.make_map(filepath)
        self.assertEqual(len(geojson['features']), 1)

class TestLinks(unittest.TestCase):

    def testLinkTxt(self):
        geojson = fdgis.make_map("https://raw.githubusercontent.com/FirstDraftGIS/fdgis/master/fdgis/tests/test.txt", debug=False)
        self.assertEqual(len(geojson['features']), 1)
        self.assertEqual(geojson['features'][0]['properties']['name'], "Australia")

    def testWithoutHttp(self):
        geojson = fdgis.make_map("raw.githubusercontent.com/FirstDraftGIS/fdgis/master/fdgis/tests/test.txt", debug=True)
        self.assertEqual(len(geojson['features']), 1)
        self.assertEqual(geojson['features'][0]['properties']['name'], "Australia")

    def testPDFLink(self):
        source = "https://www.state.gov/documents/organization/253169.pdf"
        geojson = fdgis.make_map(source, map_format="json")

    def testStructuredLinks(self):
        for extension in ["csv", "tsv", "xlsx"]:
            try:
                url = "https://raw.githubusercontent.com/FirstDraftGIS/fdgis/master/fdgis/tests/test." + extension
                geojson = fdgis.make_map(url)
                self.assertEqual(len(geojson['features']), 7)
            except Exception as e:
                print("caught exception testing url: " + url)
                print(e)
                raise e


class Timeout(unittest.TestCase):

    def testTimeout(self):
        try:
            geojson = fdgis.make_map("https://www.arlnow.com/2017/06/13/wawa-considering-arlington-as-part-of-d-c-area-expansion/", timeout=5, timeout_raises_exception=True, debug=True)
        except Exception as e:
            self.assertTrue("timeout" in str(e).lower())

        geojson = fdgis.make_map("asdifhauwehf", timeout=1)
        self.assertEqual(geojson, None)

class Combo(unittest.TestCase):

    def testTextAndTxt(self):
        txt_file = open(path_to_directory_of_this_file + "/test.txt", "rb")
        text = "I want to go to Rome, Italy"
        response = fdgis.make_map([txt_file, text], debug=True)
        features = response['features']
        self.assertTrue([f for f in features if f['properties']['name'] == "Australia"])
        self.assertTrue([f for f in features if f['properties']['name'] == "Rome"])
        txt_file.close()
        
        

# commenting out until basemaps hit production
"""
class Basemap(unittest.TestCase):

    def testBasemap(self):
        image = fdgis.make_map("South Africa, Hawaii", basemap="Stamen.Watercolor", map_format="image")
        # make sure colors match predominant basemap colors
        colors = [color for color, count Counter(image.getdata()).most_common(3)]
        self.assertTrue((251, 243, 232, 255) in colors)
        self.assertTrue((250, 242, 231, 255) in colors)
        self.assertTrue((249, 241, 230, 255) in colors)
"""

if __name__ == '__main__':
    unittest.main()
