import sys
import requests
import json 

APIkey = "jcgx5oyxczp630vm6vu9isb7vfar3z"

UPC = sys.argv[1] 
print "UPC is %s" %  UPC

#function that takes the UPC code and returns the result of the request. 
def createRequest( upc ):
    url = "https://api.barcodelookup.com/v2/products"
    parameters = {"barcode": upc, "key": APIkey } 
    return requests.get(url, params=parameters, timeout = 5)
    

response = createRequest( UPC )

print "Status code is %d" % response.status_code 

json = response.json()
print "Brand is %s" % json["products"][0]["brand"]


