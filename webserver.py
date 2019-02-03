from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT = 8080

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path=="/":
            self.path="html/home.html"

        try:
            sendReply=False
            if self.path.endswith(".html"):
                mimetype='text/html'
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

try:
    #Create a server
    server = HTTPServer(('',PORT),myHandler)
    print ('Server open on port ', PORT)

    server.serve_forever()

except KeyboardInterrupt:
    print ("Shutting down the server")
    server.socket.close()
