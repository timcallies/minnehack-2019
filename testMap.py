<<<<<<< HEAD
import geopy.distance 
import requests 

APIkey = "AIzaSyBZ_aIJmoMpqTvqfVVcwkJ11lK8QYLA35M"


def calcDistance( lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.vincenty(coords_1, coords_2).miles

def geocode( addressStr):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    parameters = {"address": addressStr, "key":APIkey }
    return requests.get(url, params=parameters, timeout = 5) 


manufacturers = { 'arizona' : ['One Arizona Plaza, 60 Crossways Park Drive, Suite 400, Woodbury, NY 11797'],
                  'driscolls' : ['S E St, Santa Maria, CA 93455', '12880 US-92, Dover, FL 33527'],
                  'dole' : ['1116 Whitmore Ave, Wahiawa, HI 96786', 'San Jose, Costa Rice', 'Medellin, Colombia'],
                  'hunts' : ['Oakdale, CA'],
                  'green giant' : ['Minnesota', 'Idaho', 'Wisconsin', 'New York', 'Peru'],
                  'bush brothers & company' : ['Augusta, WI', 'Chestnut Hill, TN'],
                  'idahoan foods' : ['Idaho Falls, ID'],
                  'tyson' : ['Albertville, AL', 'Blountsville, AL', 'Berryville, AR', 'Dexter, MO', 'New Holland, PA']
                  }
 
# st. paul = 44.9537 93.0900
print "%d" % calcDistance( 44.9537, 93.0900, 44.9591, 89.6301) 
                        
