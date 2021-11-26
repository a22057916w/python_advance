import os, time
import datetime as df
import json

mapJson = ".\mapping\sanchezPeng\mapping.json"
with open(mapJson, "r") as mappingJson:
    dict = dict(json.load(mappingJson))
    print(dict["starttime"])
    print(type(json))
