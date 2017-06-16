from sys import version_info
python_version = version_info.major

from os.path import isfile
from PIL import Image
from requests import post
if python_version == 2:
    from StringIO import StringIO
elif python_version == 3:
    from io import BytesIO
from time import sleep
if python_version == 2:
    from timeout import Timeout
elif python_version == 3:
    from .timeout import Timeout
import validators
from zipfile import ZipFile

default_url_to_server = "https://firstdraftgis.com"

def make_map(sources, map_format="geojson", basemap=None, debug=False, timeout=60, timeout_raises_exception=False, url_to_server=None):

    try:
        with Timeout(seconds=timeout):
            if debug: print("starting make_map with", sources)

            if not url_to_server:
                url_to_server = default_url_to_server

            # if passes in a singular source, turn it into a list, for for-loop below
            if not isinstance(sources, list) and not isinstance(sources, set):
                sources = [sources]

            map_format = map_format.lower()
            if map_format in ("json","pjson"):
                map_format = "geojson"
            elif map_format == "jpeg":
                map_format = "jpg"
            elif map_format in ("image", "img"):
                map_format = "png"
            elif map_format in ("coordinate-pair", "xy-pair"):
                map_format = "xy"
            elif map_format in ("shapefile", "shp", "zip"):
                map_format = "shp"

            data = {"map_format": map_format}
            files = {}

            #basemap if given
            if basemap:
                data['basemap'] = basemap

            # convert sources into format for call
            opened_files = []
            for index, source in enumerate(sources):
                source_type = str(type(source))
                if debug: print("source_type: " + source_type)
                source_type_key = "source_" + str(index) + "_type"
                source_data = "source_" + str(index) + "_data"
                if source_type in ("<type 'str'>", "<type 'unicode'>", "<class 'str'>"):
                    if isfile(source):
                        f = open(source, "rb")
                        opened_files.append(f)
                        data[source_type_key] = "file"
                        files[source_data] = f
                    elif source.startswith("http"):
                        data[source_type_key] = "link"
                        data[source_data] = source
                    elif validators.url("http://" + source):
                        source = "http://" + source
                        data[source_type_key] = "link"
                        data[source_data] = source
                    else:
                        data[source_type_key] = "text"
                        data[source_data] = source
                elif source_type in ("<class '_io.BufferedReader'>", "<class '_io.TextIOWrapper'>", "<type 'file'>"):
                    data[source_type_key] = "file"
                    files[source_data] = source
     
            if debug: print("data: " + str(data))
      
            url = url_to_server + "/request_map_from_sources"
            if debug: print("\nabout to post to " + url + " " + str(data))
            if debug: print("\ndata: " + str(data))
            if debug: print("\nfiles: " + str(files))
           


            response = post(url, data=data, files=files, timeout=timeout)
            if debug: print("response is " + str(response) + "\n")
            if debug:
                print("r.request.headers: " + str(response.request.headers))
                print("r.request.body: " + str(response.request.body))
            token = response.text
            if debug: print("token: " + str(token))

            for opened_file in opened_files:
                opened_file.close()

            for n in range(60):
                sleep(1)
                url = url_to_server + "/does_map_exist/" + token + "/" + map_format
                if debug: print("posting " + str(url))
                text = post(url, timeout=timeout).text 
                if debug: print("got " + text)
                if text == "yes":
                    url = url_to_server + "/get_map/" + token + "/" + map_format
                    stream = map_format == "shp"
                    response = post(url, stream=stream, timeout=timeout)
                    if debug: print("response: " + response.text)
                    if map_format in ("geojson", "xy"):
                       return response.json()
                    elif map_format in ("gif", "jpg", "png"):
                        if python_version == 2:
                            return Image.open(StringIO(response.content))
                        elif python_version == 3:
                            return Image.open(BytesIO(response.content))
                    elif map_format in ("csv", "tsv"):
                        return response.text
                    elif map_format == "shp":
                        if python_version == 2:
                            return ZipFile(StringIO(response.content))
                        elif python_version == 3:
                            return ZipFile(BytesIO(response.content))
                    else:
                        raise Exception("map_format (" + map_format + ") is invalid.  It must be geojson, gif, jpg, or png")
                elif text == "no":
                    pass
                else:
                    raise Exception("fdgis received the following response from the server when checking if the map is ready: " + text)

    except Exception as e:
        print("[fdgis] error in make map")
        print("[fdgis] sources:" + str(sources))
        print("[fdgis] " + str(e))
        if not ("timeout" in str(e).lower() and timeout_raises_exception == False):
            raise e
