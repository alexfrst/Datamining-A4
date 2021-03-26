import requests
import time
apikey = "efd0c606406c76609e3105eb168ebbbb"
cities = ["Suresnes", "Bagneux", "Paris", "Clichy", "Villejuif", "Issy-les-Moulineaux", "Boulogne-Billancourt", "Courbevoie", "Bagnolet", "Montreuil", "Fontenay-sous-Bois", "Asnières-sur-Seine", "Montrouge", "Nanterre", "Vincennes", "Vitry-sur-Seine", "Saint-Denis", "Le Kremlin-Bicêtre", "Maisons-Alfort", "Argenteuil", "Chaville", "Cachan", "Colombes", "Ivry-sur-Seine", "Aubervilliers", "Nogent-sur-Marne", "Le Pré-Saint-Gervais", "Joinville-le-Pont", "Arcueil", "La Garenne-Colombes", "Malakoff", "Romainville", "Pantin", "Levallois-Perret", "Saint-Mandé", "Neuilly-sur-Seine", "Rosny-sous-Bois", "Alfortville", "Vanves", "Champigny-sur-Marne", "Gentilly", "Les Lilas", "Rueil-Malmaison", "Saint-Cloud", "Gennevilliers", "Meudon", "Charenton-le-Pont", "Bourg-la-Reine", "Choisy-le-Roi", "Fontenay-aux-Roses", "Puteaux", "Clamart", "Saint-Maurice", "Sèvres", "Sceaux", "Villeurbanne", "Lyon 5 ème", "Lyon 3 ème", "Lyon 7 ème", "Lyon 6 ème", "Lyon 4 ème", "Lyon 1 er", "Lyon 8 ème", "Caluire-et-cuire", "Lyon 9 ème", "La mulatiere", "Lyon 2 ème", "Pierre-benite", "Bron", "Vaulx-en-velin", "Fontaines-sur-saone", "Neuville-sur-saone", "Saint-priest", "Tassin-la-demi-lune", "Venissieux", "Saint-fons", "Collonges-au-mont-d'or", "Sainte-foy-les-lyon", "Saint-cyr-au-mont-d'or", "Rillieux-la-pape", "Saint-genis-laval", "Saint-didier-au-mont-d'or", "Decines-charpieu", "Oullins", "Couzon-au-mont-d'or", "Ecully", "Albigny-sur-saone", "Rennes"]
mapper = {"Clear":"brightness-high","Drizzle":"cloud-drizzle","Thunderstorm":"cloud-lightning","Rain":"rain-heavy",
          "Snow":"cloud-snow","Atmosphere":"cloud-haze", "Clouds":"clouds"}


class Weather():
    def __init__(self):
        self.weatherTab = []

    def loadData(self):
        file = open("weather.save","r").read()
        self.weatherTab = [[elem.split(",")[0],elem.split(",")[1]] for elem in file.split("\n")]
    def exportData(self):
        file = open("weather.save","w",encoding="utf8")
        file.write("\n".join([",".join(elem) for elem in self.weatherTab]))

    def queryData(self):
        size = int(len(cities)/3)
        batches = [cities[:size],cities[size:2*size],cities[2*size:]]
        for batche in batches:
            for city in batche:
                print(city)
                if("lyon" in city.lower()):
                    result = requests.get("https://api.openweathermap.org/data/2.5/weather",
                                          params={"appId": apikey, "q": "Lyon", "units": "metric"})
                    self.weatherTab.append([city, mapper[result.json()["weather"][0]["main"]]])
                else:
                    result = requests.get("https://api.openweathermap.org/data/2.5/weather",
                                          params={"appId": apikey, "q": city, "units": "metric"})
                    self.weatherTab.append([city, mapper[result.json()["weather"][0]["main"]]])
                print(self.weatherTab[-1])
            time.sleep(65)

