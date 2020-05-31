import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
from io import BytesIO
import socketserver
import random

import pannels

hostName = "127.0.0.1"
serverPort = 80
storageFile = "shortens.yml"

def genRandomUUID(): #Generate the link UUID
    while True:
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_"
        UUID = ""
        for i in range(0, 11):
            UUID += random.choice(chars)
        
        if not UUID in getAllShortUUIDS(): #Check if the UUID is already used in the databace
            break
    return UUID

def getAllShortUUIDS(): #Return all the UUIDs
    if os.path.exists(storageFile):
        with open(storageFile) as f:
            lines = f.read().splitlines()
        
        ids = []
        for i in lines:
            ids.append(i)
        
        return ids
    else:
        return []

def convertUUID(uuid): #Convert UUID to the url
    if os.path.exists(storageFile):
        with open(storageFile) as f:
            lines = f.read().splitlines()

        for line in lines:
            splitData = line.split(":", 1)
            if splitData[0] == uuid:
                return splitData[1]
        return None
    else:
        return None

def handleGetRequest(request, self):
    if len(request) == 0:
        pannels.createShortUrl(self)
        return

    if convertUUID(request[0]): #Valid UUID found, send user to URL
        redirectUrl = convertUUID(request[0])
        self.wfile.write(bytes('<script>window.location = "' + redirectUrl + '";</script>', "utf-8"))
    else:
        pannels.shortNotExists(self)
        

def handlePostRequest(self):
    content_length = int(self.headers['Content-Length'])
    requestRaw = self.rfile.read(content_length)
    request = requestRaw.decode("utf-8")
    
    response = BytesIO()

    if request.startswith("ShortUrl:"):
        splits = request.split(":", 1)
        shortUrl = splits[1]
        with open(storageFile, "a") as f:
            UUID = genRandomUUID()
            if shortUrl.startswith("http://") or shortUrl.startswith("https://"):
                f.write(UUID + ":" + shortUrl + "\n")
            else:
                f.write(UUID + ":https://" + shortUrl + "\n")
        response.write(bytes("http://127.0.0.1/" + UUID, "utf-8"))
        self.wfile.write(response.getvalue())

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        requestList = list(filter(None, str(self.path).split("/")))
        handleGetRequest(requestList, self)
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        handlePostRequest(self)

webServer = HTTPServer((hostName, serverPort), WebServer)
try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped")