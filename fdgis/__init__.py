from json import loads
from os.path import isfile
from requests import post
from time import sleep

url_to_server = "https://dev.firstdraftgis.com"

def make_map(source=None, sources=None, format="geojson", debug=True):

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
 
    if debug: print "data:", data
    
    url = url_to_server + "/request_map_from_sources"
    if debug: print "\nabout to post to ", url, data
    response = post(url, data=data, files=files)
    if debug: print "response", response, "\n"
    token = response.text
    if debug: print "token:", token

    for n in range(60):
        sleep(1)
        url = url_to_server + "/does_map_exist/" + token + "/geojson"
        if debug: print "posting " + url
        text = post(url).text 
        if debug: print "got " + text
        if text == "yes":
            url = url_to_server + "/get_map/" + token + "/geojson"
            if debug: print "posting " + url
            return loads(post(url).text)
            
