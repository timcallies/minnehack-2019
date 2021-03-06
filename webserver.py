#pip install zbar-py
#pip install imageio
#pip install pillow

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import os
import cgi
import numpy
import math
import zbar
import zbar.misc
import base64
from PIL import Image
import imageio
import upcReader
import geoloc
import mapsearcher

port = os.environ.get('PORT')
if (port==None):
    port=3000
else:
    port = int(port)

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path=="/":
            self.path="html/home.html"

        try:
            sendReply=False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply=True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply=True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply=True

            if sendReply==True:
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File not found: ' % self.path)

    def do_POST(self):
        if(self.path=="/submit"):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-type'],
                }
            )
            imageData = form['img'].value.lstrip("data:image/png;base64")
            imageBytes = bytes(imageData, 'utf-8')
            with open("imageToSave.png", "wb") as f:
                f.write(base64.decodebytes(imageBytes))


            img = Image.open("imageToSave.png")
            change_contrast(img,100)
            image = numpy.array(img)

            if len(image.shape) == 3:
                image = zbar.misc.rgb2gray(image)
            scanner = zbar.Scanner()
            results = scanner.scan(image)
            hasResult = False
            if(len(results)>0):
                for result in results:
                    if(result.type=="UPC-A"):

                        print(result.data)
                        UPCstr = result.data

                        #get the details about this UPC
                        UPC = int(UPCstr)
                        item = upcReader.newProduce(UPC)
                        if item != -1:
                            hasResult=True
                            item.toString()
                            self.send_response(200)
                            self.send_header('Content-type','text/html')
                            self.end_headers()

                            self.wfile.write("<html><header><title>Sustainability Scanner</title></header><link href='https://fonts.googleapis.com/css?family=Staatliches' rel='stylesheet'><style>@import url('/style.css');</style><body><div id='main'>".encode())
                            if(item.name!=""):
                                self.wfile.write(("<h1>"+item.name+"</h1>").encode())
                            if(item.upc!=""):
                                self.wfile.write(("<li>UPC: "+item.upc+"</li>").encode())
                            if(item.brand!=""):
                                self.wfile.write(("<li>Brand: "+item.brand+"</li>").encode())
                            if(item.manufacturer!=""):
                                self.wfile.write(("<li>Manufacturer: "+item.manufacturer+"</li>").encode())


                            userLat = form['latitude'].value
                            userLng = form['longitude'].value

                            mapsearch = (mapsearcher.findLocalProduct(item.name,userLat,userLng))
                            if mapsearch != "":
                                self.wfile.write(("<li>Check out: "+mapsearch+"</li>").encode())

                            weight = item.weight

                            co2Grams = geoloc.c02calc( item.manufacturer, weight, userLat, userLng)
                            self.wfile.write(("<li>Grams of CO2: " +str(co2Grams)+"g</li>").encode())


                            distance = geoloc.getDistance(item.manufacturer,  userLat, userLng)
                            self.wfile.write(("<li>Distance from origin: " +str(distance)+"km</li>").encode())


                            if co2Grams > 20:
                                self.wfile.write(("<li>Your food choice produces a very high amount of CO2 emissions</li>").encode())
                            elif co2Grams > 10 and co2Grams <= 20:
                                self.wfile.write(("<li>Your food choice produces a moderate amount of CO2 emissions</li>").encode())
                                self.wfile.write(("<li>Not bad, but you could do better!</li>").encode())
                            elif co2Grams <= 10:
                                self.wfile.write(("<li>Your food choice produces a low amount of CO2 emissions</li>").encode())
                                self.wfile.write(("<li>Well done, you're saving the planet!!</li>").encode())



                            self.wfile.write("</div></body></html>".encode())

            if not hasResult:
                self.send_response(200)
                self.send_header('Location','/')
                f = open(curdir + sep + 'html/home.html', 'rb')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()


try:
    #Create a server
    server = HTTPServer(('',port),myHandler)
    print ('Server open on port ', port)

    server.serve_forever()

except KeyboardInterrupt:
    print ("Shutting down the server")
    server.socket.close()
