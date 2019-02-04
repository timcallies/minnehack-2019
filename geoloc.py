import geopy.distance
import requests
import os
import pickle

#for google cloud platform
APIkey = ""


def calcDistance( lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.vincenty(coords_1, coords_2).km

def geocode( addressStr):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    parameters = {"address": addressStr, "key":APIkey }

    response = requests.get(url, params=parameters, timeout = 5)

    try:
        json = response.json()
        if response.status_code != 200:
            print("Was not able to parse json object from API response. Response code = {}. UPC is {}".format(response.status_code, UPC))
            exit(1)
        else:
            return json
    except ValueError:
        print("Was not able to parse json object from API response. Response code = {} UPC = {}".format(response.status_code, UPC))
        exit(1)


#use for mapping a list of addresses to a list of tuple coords
# form of (lat, long)
def addressToGeo( lstOfAddresses ):
    result = []
    for x in lstOfAddresses:
        #print( "Address is {}".format(x))

        #get the lat and long from the json
        response = geocode(x)
        location = response["results"][0]["geometry"]["location"]
        coords   = (location["lat"], location["lng"])
        result.append( coords )

        return result


def printDictionary( dictonary ):
    for k,v in dictonary.items():
        print("Key: %s" .format(k) )
        for item in v:
            print(item)


# st. paul = 44.9537 93.0900
#print "%d" % calcDistance( 44.9537, 93.0900, 44.9591, 89.6301)




# mf = manufacturer name
def getDistance( mfName, userLat, userLng ):

    manufacturers = { 'ferolito vultaggio & sons' : ['One Arizona Plaza, 60 Crossways Park Drive, Suite 400, Woodbury, NY 11797'],
            "driscoll's" : ['S E St, Santa Maria, CA 93455', '12880 US-92, Dover, FL 33527'],
            'dole' : ['1116 Whitmore Ave, Wahiawa, HI 96786', 'San Jose, Costa Rice', 'Medellin, Colombia'],
            "hunt's" : ['554+S+Yosemite+Ave,+Oakdale,+CA+95361'],
            'green giant' : ['1126+Green+Giant+Ln,+Blue+Earth,+MN+56013'],
            'bush brothers & company' : ['600+Bush+Brothers+Drive,+Augusta,+WI+54722', '3304+Chestnut+Hill+Rd,+Dandridge,+TN+37725'],
            'idahoan foods' : ['529+N+3500+E,+Lewisville,+ID+83431'],
            'tyson' : ['6600+US-431,+Albertville,+AL+35950', '67240+Main+St,+Blountsville,+AL+35031', '110+W+Freeman+Ave,+Berryville,+AR+72616', '1001+E+Stoddard+St,+Dexter,+MO+63841', '403+S+Custer+Ave,+New+Holland,+PA+17557']

            }

    #HTML5 will default to 0,0 if the user declines.
    if userLat == 0 and userLng == 0:
        print("User did not provide their location" )
        return -1;

    #if the addresses file already exitst then open for appending
    #otherwise create the file and write the addresses.
    if( os.path.isfile( "./addresses.pickle" ) ):
        addresses = open( "./addresses.pickle", "rb")

        try:
            #load the dict of gpucords
            manufacturers = pickle.load( addresses )
        except EOFError:
            os.remove("addresses.pickle")
            print("was not able to load file of locations. Run the server again to regenerate")
            addresses.close()
            exit(1)

        addresses.close()
    else:
        addresses = open( "./addresses.pickle", "wb")

        print("Converting the addresses to geolocations....")
        geolocations = dict(map( lambda kv: ( kv[0], addressToGeo(kv[1]) ) , manufacturers.items() ))

        #save the geocode
        pickle.dump( geolocations, addresses)

        addresses.close()
        manufacturers = geolocations

    #get the closest manufactor location
    #actually just get the first item in the list
    origin = manufacturers[mfName][0]

    return abs(calcDistance( userLat, userLng, origin[0], origin[1] ) )


def c02calc( mfName, weight, userLat, userLng ):
    #default to a small item of 30 grams ~1 oz if no weight is provided.
    if weight == 0:
        weight = 30 

    distance = getDistance( mfName, userLat, userLng)

    #average cargo plane average emissions per metric ton per km Source Lufthansa Air cargo
    airEmision = 500 # 500g * weight in tons * km
    gramsPerTon = 907185

    emisions = airEmision * ( weight / gramsPerTon ) * distance
    return emisions # returns the total amount of co2 in grams
