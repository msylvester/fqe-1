#FczaT2Z0fRE1yzaMWJSWAlkvFKTXfOaHD8SMf6sFwY6BN1hB
import requests

#API_TOKEN = "FczaT2Z0fRE1yzaMWJSWAlkvFKTXfOaHD8SMf6sFwY6BN1hB"

#MARK: class Location
# This class abstracts the properties of a location object sent from messenger app on ios

class Location:
    def __init__(self, name, longitude, lat, url, time, id):
        self.name = name
        self.long = longitude
        self.lat = lat

        self.url = url
        self.time = time
        self.id = id

    def getName(self):
        return self.name

    def getURL(self):
        return self.url

    def getLat(self):
        return self.lat

    def getLong(self):
        return self.long

    def getDataType(self):
    	return "location"

    def getID(self):
        return self.id




