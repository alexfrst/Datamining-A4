import requests
from Station import Station


class City:
    def __init__(self,name):
        self.stations = []
        if name == "Paris" :
            self.buildParis()
        elif name == "Lyon" :
            self.buildLyon()
        elif name == "Rennes":
            self.buildRennes()


    def buildJcDecaux(self):
        requests.get();

    def buildParis(self):
        json = requests.get("https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&rows=1000").json()["records"]
        for fields in json:
            station = fields["fields"]
            parameters = {
                "network":"Paris",
                "name":station["name"],
                "number":int(station["stationcode"]),
                "lat":station["coordonnees_geo"][0],
                "long":station["coordonnees_geo"][1],
                "stands":station["capacity"],
                "availablestands":station["numdocksavailable"],
                "totalbikes": station["numbikesavailable"],
                "availableBikes":station["ebike"],
                "availableEBikes":station["mechanical"],
                "city":  station["nom_arrondissement_communes"]
            }
            self.stations.append(Station(**parameters))

    def buildLyon(self):
        json = requests.get("https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171").json()["features"]
        for fields in json:
            station = fields["properties"]
            parameters = {
                "network":"Lyon",
                "name":station["name"],
                "number":int(station["number"]),
                "lat":station["lat"],
                "long":station["lng"],
                "stands":station["bike_stands"],
                "availablestands":station["available_bike_stands"],
                "totalbikes": station["available_bikes"],
                "availableBikes":station["available_bikes"],
                "availableEBikes":0,
                "city":station["commune"].capitalize()
            }
            self.stations.append(Station(**parameters))

    def buildRennes(self):
        json = requests.get(
            "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel").json()[
            "records"]
        for fields in json:
            station = fields["fields"]

            parameters = {
                "network": "Rennes",
                "name": station["nom"],
                "number": int(station["idstation"]),
                "lat": station["coordonnees"][0],
                "long": station["coordonnees"][1],
                "stands": station["nombreemplacementsactuels"],
                "availablestands": station["nombreemplacementsdisponibles"],
                "totalbikes": station["nombrevelosdisponibles"],
                "availableBikes": station["nombrevelosdisponibles"],
                "availableEBikes": 0,
                "city":"Rennes"
            }
            self.stations.append(Station(**parameters))
