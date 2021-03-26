from ontology import ontology


onto = ontology()
onto.loadCity("Paris")
onto.loadCity("Lyon")
onto.loadCity("Rennes")
onto.sendData()