import geopy.distance 
import requests 
import os 
import pickle 

#for google cloud platform 
APIkey = "AIzaSyBZ_aIJmoMpqTvqfVVcwkJ11lK8QYLA35M"

manufacturers = { 'arizona' : ['One Arizona Plaza, 60 Crossways Park Drive, Suite 400, Woodbury, NY 11797'],
                  'driscolls' : ['S E St, Santa Maria, CA 93455', '12880 US-92, Dover, FL 33527'],
                  'dole' : ['1116 Whitmore Ave, Wahiawa, HI 96786', 'San Jose, Costa Rice', 'Medellin, Colombia'],
                  }



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
        print( "Address is {}".format(x))

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

    #HTML5 will default to 0,0 if the user declines. 
    if userLat == 0 and userLng == 0:
        print("User did not provide their location" )
        return -1;

    #if the addresses file already exitst then open for appending
    #otherwise create the file and write the addresses. 
    if( os.path.isfile( "./addresses.pickle" ) ):
        addresses = open( "./addresses.pickle", "rb")

        #load the dict of gpucords
        manufacturers = pickle.load( addresses ) 
        addresses.close()
    else:
        addresses = open( "./addresses.pickle", "wb") 
        
        print("Converting the addresses to geolocations....")
        #convert addresses to geocode
        geolocations = dict(map( lambda kv: ( kv[0], addressToGeo(kv[1]) ) , manufacturers.iteritems() ))

        #save the geocode  
        pickle.dump( geolocations, addresses)

        addresses.close()
        manufacturers = geolocations 

    #get the closest manufactor location
    #actually just get the first item in the list
    origin = manufacturers[mfName][0]
    
    return calcDistance( userLat, userLng, origin[0], origin[1] ) 


#distance = getDistance( "dole", (44.9537, 93.0900) )
#print "Distance from Dole is: %dkm" % distance



