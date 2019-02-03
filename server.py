import sys
import requests

APIkey = "jcgx5oyxczp630vm6vu9isb7vfar3z"


UPC = sys.argv[1]
print "UPC is %s\n" %  UPC



response = requests.get("https://api.barcodelookup.com/v2/products?barcode=715756100019&key=jcgx5oyxczp630vm6vu9isb7vfar3z")

print "Status code is %d\n" % response.status_code
print "Result is %s\n" % response.content
