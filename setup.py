from distutils.core import setup

setup(
  name = 'fdgis',
  packages = ['fdgis'],
  package_dir = {'fdgis': 'fdgis'},
  package_data = {'fdgis': ['__init__.py', 'timeout/__init__.py']},
  version = '2.5',
  description = 'Makes the first draft of your map',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/FirstDraftGIS/fdgis',
  download_url = 'https://github.com/FirstDraftGIS/fdgis/tarball/download',
  keywords = ['geocoding','geojson','gis','maps','nlp','python'],
  classifiers = [],
  install_requires=["Pillow", "requests"]
)
