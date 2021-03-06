:warning: The public API no longer works because the EC2 server was costing too much.  I'm rewriting the core service using Lambda, which will take several months.  Let me know if you have any thoughts or want help setting up your own first draft server. You can contact me at daniel.j.dufour@gmail.com and I apologize for the inconvenience.  Also, would love some help with this if you want to contribute :-) 

# fdgis
**fdgis** is a Python library that **makes maps**.

## Installation
```
pip install fdgis
```

## Use
### GeoJSON
```
from fdgis import make_map
text = "He visited New Jersey last year."
geojson = make_map(text, map_format="geojson")
```
```
{u'type': u'FeatureCollection', u'features': [{u'geometry': {u'type': u'GeometryCollection', u'geometries': [{u'type': u'Point', u'coordinates': [-74.49987, 40.16706]}]}, u'type': u'Feature', u'properties': {u'geonameid': 5101760, u'confidence': 0.0241, u'pcode': None, u'name': u'New Jersey', u'country_code': u'US'}}]}
```

### Image
```
from fdgis import make_map
text = "He visited Arlington, VA"
image = make_map(text, map_format="image")
image.save("/tmp/map.png")
```
<img src="https://raw.githubusercontent.com/FirstDraftGIS/fdgis/master/arlington.png" width="700px">

## Features
| Languages Supported |
| ------------------- |
| Arabic |
| English |
| Spanish|

## How it works
**fdgis** works by sending requests to First Draft GIS servers.  First Draft GIS is an open-source artificial intelligence that makes maps.  The source code for First Draft GIS can be found at https://github.com/FirstDraftGIS/firstdraft.  By default the library works by sending a request to the public First Draft GIS server at https://firstdraftgis.com.  You can point fdgis to your own server in the following way
```
import fdgis
fdgis.default_url_to_server = "https://yourownserverhere.com"
geojson = fdgis.make_map("He took a long train ride to Columbus, OH.")
```
If you want to point **fdgis** to the more advanced but highly unstable dev version, you would do the following:
```
import fdgis
fdgis.default_url_to_server = "https://dev.firstdraftgis.com"
geojson = fdgis.make_map("He took a long train ride to Columbus, OH.")
```

## Timeout
You can specify a timeout for the make_map method.  If the method doesn't make a map in the amount of seconds you specify it returns `None`.  If you prefer it to throw a Timeout error instead, you can write set `timeout_raises_exception` to `True`.  See the example below:
```
from fdgis import make_map
try:
    geojson = make_map("Houston has the best food.", timeout=3, timeout_raises_exception=True)
except Excpetion as e:
    print "UH OH. fdgis threw an exception"
```

## End User Timezone
You can specify the timezone if made by an end user by using the end_user_timezone field.
```
from fdgis import make_map
geojson = make_map("I like Clarendon", end_user_timezone="America/New_York")
```

## Case Insensitivity
You can resolve places without case sensitivity.
```
from fdgis import make_map
geojson = make_map("bethesda", case_insensitive=True)
```

## Testing
To test the package run
```
python -m unittest fdgis.tests.test
```

If you have fdgis installed on a First Draft GIS server and want to use it to test your local server, run
```
python -m fdgis.tests.test_locally
```

## Input Data Formats Supported
These are the types of data that FDGIS can create a map from

| Format | Status |
| ------ | ------ |
| CSV | Yes |
| DOC | No |
| DOCX | Yes |
| HTML | Yes |
| PDF | Yes |
| TXT | Yes |
| TSV | Yes |
| XLS | No |
| XLSM | Yes |
| XLSX | Yes |
| XLTM | Yes |
| XLTX | Yes |

## Help
If you have any questions, don't hesitate to contact the author at daniel@firstdraftgis.com or open up an issue on the GitHub Repo at https://github.com/FirstDraftGIS/fdgis/issues
