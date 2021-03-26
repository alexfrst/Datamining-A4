class Station:

    def __init__(self,city,name, number, lat, long,stands,availablestands, totalbikes, availableBikes,network, availableEBikes=0):
        self.name = name
        self.number = number
        self.lat = lat
        self.long = long
        self.stands = stands
        self.availableStands = availablestands
        self.totalbikes = totalbikes
        self.bikes = availableBikes
        self.ebikes = availableEBikes
        self.id = str(network)+str(number)
        self.network = network
        self.city = city

    def __str__(self):
        return " ".join([str(self.name),str(self.number),str(self.lat),str(self.long),str(self.stands),str(self.availableStands),str(self.totalbikes),str(self.bikes),str(self.ebikes),str(self.id)])