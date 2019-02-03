import requests

APIkey = "3tg1gkl1v84sc51ub7yinnx7iozrk3"


'''
=== FORMAT OF PRODUCE ITEM ===
    name    <- Name of the product
    upc     <- UPC number
    brand   <- Brand name
    manufacturer <- Name of the manufacturer

    optional
    ingrediants   <- a list of ingrediants in the product
    nutrition <- name of the manufacturer


    All strings are lowercase

'''

class produceItem:
    def __init__(self, name, upc, brand, manufacturer):
        self.name = name.lower()
        self.upc = upc.lower()
        self.brand = brand.lower()
        self.manufacturer = manufacturer.lower()

        #possible null values
        self.weight = 0 
        self.nutrition = []
        self.ingrediants = []

    def addNutrition( self, nutrition ):
        #do any necassary string formating
        nutrition = nutrition.lower().split(", ")

    def addIngrediants( self, ingrediants ):
        self.ingrediants = ingrediants.lower().split(", ")

    def addWeight(self, weight):
        self.weight = 10

    def toString(self):
        print ("Name: {}\n\t UPC: {}\n\t Brand: {} \n\t Manufacturer: {}\n".format(self.name, self.upc, self.brand, self.manufacturer) )
        if len( self.nutrition ) != 0:
            print ("\tNutrition:")
            for x in range( len(self.nutrition) ):
                print ("\t\t %s" % self.nutrition[x] )

        if len(self.ingrediants) != 0:
                print ("\tIngrediants:")
                for x in range( len(self.ingrediants) ):
                    print ("\t\t %s" % self.ingrediants[x])



#function that takes the UPC code and returns the result of the request.
def createRequest( upc ):
    url = "https://api.barcodelookup.com/v2/products"
    parameters = {"barcode": upc, "key": APIkey }
    return requests.get(url, params=parameters, timeout = 5)



def newProduce( UPC ):

    #send out the request to the UPC API
    response = createRequest( UPC )

    # Error check JSON
    try:
        json = response.json()
        if response.status_code != 200:
            print ("Was not able to parse json object from API response. Response code = %d. UPC is %s" % (response.status_code, UPC))
            return -1

    except ValueError:
        print ("Was not able to parse json object from API response. Response code = %d UPC = %s" % (response.status_code, UPC))
        return -1

    product = json["products"][0]
    item = produceItem( product["product_name"], product["barcode_number"], product["brand"], product["manufacturer"])


    if product["nutrition_facts"] != "":
        item.addNutrition( product["nutrition_facts"] )

    if product["ingredients"] != "":
        item.addIngrediants( product["ingredients"] )

    if product["weight"] != "": 
        item.addWeight( product["weight"] )

    return item
