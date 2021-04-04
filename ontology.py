import requests
from Weather import Weather
from City import City
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import XSD
from rdflib.plugins.stores import sparqlstore

type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
label = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
network = URIRef("http://example.org/network")
network = URIRef("http://dbpedia.org/ontology/network")
city = URIRef("http://dbpedia.org/ontology/city")
country = URIRef("http://dbpedia.org/ontology/country")
docks = URIRef("http://example.org/docks")
available = URIRef("http://example.org/available")
bikes = URIRef("http://example.org/bikes")
ebikes = URIRef("http://example.org/ebikes")
total = URIRef("http://example.org/total")
id = URIRef("http://example.org/id")
lat = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat")
long = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long")


class ontology:


    def __init__(self):
        self.g = Graph()
        self.cityid = {}


    def loadCity(self,name):
        data = City(name).stations
        for station in data:
            stationId = URIRef("http://example.org/station/"+station.id)
            self.g.add((stationId, label, Literal(station.name)))
            self.g.add((stationId, city, Literal(station.city)))
            self.g.add((stationId, network, Literal(station.network)))
            self.g.add((stationId, country, Literal("France")))
            self.g.add((stationId, docks, Literal(station.stands, datatype=XSD.integer)))
            self.g.add((stationId, available, Literal(Literal(station.availableStands))))
            self.g.add((stationId, bikes, Literal(station.bikes, datatype=XSD.integer)))
            self.g.add((stationId, ebikes, Literal(station.ebikes, datatype=XSD.integer)))
            self.g.add((stationId, total, Literal(station.totalbikes, datatype=XSD.integer)))
            self.g.add((stationId, lat, Literal(station.lat, datatype=XSD.float)))
            self.g.add((stationId, long, Literal(station.long, datatype=XSD.float)))

    def loadWeather(self):
        weather = Weather()
        weather.loadData()
        for elem in weather.weatherTab:
            city = URIRef("http://example.org/station/" + elem[0])
            weather = URIRef("http://example.org/weather/")
            self.g.add((city,weather,Literal(elem[1])))


    def sendData(self):
        data = self.g.serialize(format="turtle").decode("utf-8")
        print(data)
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        file = open("save.ttl","w",encoding="utf8")
        file.write(data)
        file.close()

        data = open('save.ttl', "rb")
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        r = requests.put('http://localhost:3030/DataminingProject/data?default', data=data, headers=headers)
        print(r.status_code)

    def exportData(self):
        data = self.g.serialize(format="turtle").decode("utf-8")
        print(data)
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        file = open("save.ttl", "w", encoding="utf8")
        file.write(data)
        file.close()

    def readAndSave(self):
        data = open('save.ttl', "rb")
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        r = requests.put('http://localhost:3030/DataminingProject/data?default', data=data, headers=headers)
        print(r.status_code)



