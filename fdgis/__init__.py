from json import loads
from os.path import isfile
from PIL import Image
from requests import post
from StringIO import StringIO
from time import sleep

url_to_server = "https://dev.firstdraftgis.com"

def make_map(source=None, sources=None, map_format="geojson", debug=True):

    if debug: print "starting make_map with", source, sources

    if not source and not sources:
        print "You forgot to include some sources, which your map will be based on!"
        print "If you have any questions, consult the documentation or email daniel@firstdraftgis.com :)"
        raise Exception("sources missing")

    if not sources:
        sources = []

    if source:
        if debug: print "appending source to sources:", sources
        sources.append(source)

    map_format = map_format.lower()
    if map_format in ("json","pjson"):
        map_format = "geojson"
    elif map_format == "jpeg":
        map_format = "jpg"
    elif map_format in ("image", "img"):
        map_format = "png"

    # convert sources into format for call
    data = {}
    files = {}
    for index, source in enumerate(sources):
        source_type = "source_" + str(index) + "_type"
        source_data = "source_" + str(index) + "_data"
        if isinstance(source, unicode) or isinstance(source, str):
            if isfile(source):
                f = open(source)
                data[source_type] = "file"
                files[source_data] = f
            elif source.startswith("http"):
                data[source_type] = "link"
                data[source_data] = source
            else:
                data[source_type] = "text"
                data[source_data] = source
        elif isinstance(source, file):
            data[source_type] = "file"
            files[source_data] = source
 
    if debug: print "data:", data
    
    url = url_to_server + "/request_map_from_sources"
    if debug: print "\nabout to post to ", url, data
    response = post(url, data=data, files=files)
    if debug: print "response", response, "\n"
    token = response.text
    if debug: print "token:", token

    for n in range(60):
        sleep(1)
        url = url_to_server + "/does_map_exist/" + token + "/" + map_format
        if debug: print "posting " + url
        text = post(url).text 
        if debug: print "got " + text
        if text == "yes":
            url = url_to_server + "/get_map/" + token + "/" + map_format
            if debug: print "posting " + url
            response = post(url)
            if map_format == "geojson":
                return loads(response.text)
            elif map_format in ("gif", "jpg", "png"):
                return Image.open(StringIO(response.content))
            else:
                raise Exception("map_format (" + map_format + ") is invalid.  It must be geojson, gif, jpg, or png")
        elif text == "no":
            pass
        else:
            raise Exception("fdgis received the following response from the server when checking if the map is ready: " + text)
