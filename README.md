[![Build Status](https://travis-ci.org/FirstDraftGIS/fdgis.svg?branch=master)](https://travis-ci.org/FirstDraftGIS/fdgis)

# fdgis
**fdgis** is a Python library that **makes maps**.

## Installation
```
pip install fdgis
```

## Use
###GeoJSON
```
from fdgis import make_map
text = "He visited New Jersey last year."
geojson = make_map(text, map_format="geojson")
```
```
{u'type': u'FeatureCollection', u'features': [{u'geometry': {u'type': u'GeometryCollection', u'geometries': [{u'type': u'Point', u'coordinates': [-74.49987, 40.16706]}]}, u'type': u'Feature', u'properties': {u'geonameid': 5101760, u'confidence': 0.0241, u'pcode': None, u'name': u'New Jersey', u'country_code': u'US'}}]}
```

###Image
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
fdgis.url_to_server = "https://yourownserverhere.com"
geojson = fdgis.make_map("He took a long train ride to Columbus, OH.")
```

## Testing
To test the package run
```
python -m unittest fdgis.tests.test
```

## Input Data Formats Supported
These are the types of data that FDGIS can create a map from

| Format | Status |
| ------ | ------ |
| CSV | Yes |
| DOC | Soon |
| DOCX | Yes |
| HTML | Yes |
| PDF | Yes |
| TXT | Yes |
| TSV | Yes |
| XLS | Soon |
| XLSX | Yes |

## Help
If you have any questions, don't hesitate to contact the author at daniel@firstdraftgis.com or open up an issue on the GitHub Repo at https://github.com/FirstDraftGIS/fdgis/issues
