__author__ = 'don'
import xmltodict
import geojson
import json
from datetime import datetime

from collections import OrderedDict
from operator import attrgetter

with open('inspections.xml') as fd:
    obj = xmltodict.parse(fd.read())

features = []

for business in obj['Business_Inspection_Violation']['Business']:
    try:
        lat = float(business['Latitude'])
        lng = float(business['Longitude'])
        name = business['Name']
        address = business['Address']
        description = business['Description']
    except TypeError:
        pass
    else:
        try:
            inspections = business['Inspection']
            latestDate = datetime.min
            result = ""
            for inspection in inspections:
                inspDate = datetime.strptime(inspection["Inspection_Date"],"%m/%d/%Y")
                if (inspDate > latestDate):
                    latestDate = inspDate
                    result = inspection["Inspection_Result"]
        except (TypeError, KeyError):
            pass
        else:
            score = inspection["Inspection_Score"]
            theDate = latestDate.strftime("%m/%d/%Y")
            features.append(geojson.Feature(geometry=geojson.Point((lng, lat)), id=name, properties={"Name":name, "Address":address, "Description":description, "Inspected":theDate, "Result":result, "Score":score}))

fc = geojson.FeatureCollection(features)

print geojson.dumps(fc, indent=2)
