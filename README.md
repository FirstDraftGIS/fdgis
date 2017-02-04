# fdgis
FDGIS is the Python library used to interface with your First Draft GIS server  

# Installation
```
pip install fdgis
```

# Use
```
from fdgis import make_map
text = "He visited New Jersey last year."
geojson = make_map(text)
```

```
{u'type': u'FeatureCollection', u'features': [{u'geometry': {u'type': u'GeometryCollection', u'geometries': [{u'type': u'Point', u'coordinates': [-74.49987, 40.16706]}]}, u'type': u'Feature', u'properties': {u'geonameid': 5101760, u'confidence': 0.0241, u'pcode': None, u'name': u'New Jersey', u'country_code': u'US'}}]}
```

# Features
| Languages Supported |
| ------------------- |
| Arabic |
| English |
| Spanish|

# Testing
To test the package run
```
python -m unittest fdgis.tests.test
```
