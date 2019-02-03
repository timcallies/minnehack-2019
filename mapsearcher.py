import requests

APIkey = "AIzaSyBzZ6ovLHt2ZP0iP212R7GDGkIZH0py2Hs"

def findLocalProduct(name,latitude,longitude):
    query = ""
    if("berry" in name or "berries" in name):
        query = "berry farm"
    elif("apple" in name):
        query = "apple orchard"
    elif("broccoli" in name):
        query = "broccoli farm"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    if(query == ""):
        #Item does not have any replacements
        return ""


    location = latitude+","+longitude
    parameters = {
        "location": location,
        "radius": "5000",
        "query": query,
        "key": APIkey
    }

    response = requests.get(url, params=parameters, timeout = 5)

    try:
        json = response.json()
        if response.status_code != 200:
            print("Was not able to parse json object from API response. Response code = {}. UPC is {}".format(response.status_code, UPC))
            return ""
        else:
            return json["results"][0]["name"]
    except ValueError:
        print("Was not able to parse json object from API response. Response code = {} UPC = {}".format(response.status_code, UPC))
        return ""
