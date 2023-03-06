from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 5000

def parser(query):
    splitted = query.split('&')
    ret = {}
    for pair in splitted:
        kvp = pair.split('=')
        ret[kvp[0]]=kvp[1]
    return 

users=[
    {"username":"admin",
     "password":"admin"}
]

def authenticate(userInfo):
    for user in users:
        if user["username"] == userInfo["username"] and user["password"] == userInfo["password"]:
            return True
    return False

#Users
def getUsers():
    members=[]
    for user in users:
        members.append(user["username"])
    return ','.join(members)


routes = {
    "static": {
        "/": open("index.html").read(),
        "/login": open("login.html").read(),
        "/register": open("register.html").read(),
        #"/test": open("CSC450 assignment12.html").read()
    },
    "api": {   
     "/api/getUsers":getUsers()
    } 
}    

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes["static"]:
            self.http_header(200, "text/html")
            self.wfile.write(bytes(routes["static"][self.path], "utf-8"))
        elif self.path.startswith("/api"):
            self.http_header(200, "application/json")
            self.wfile.write(bytes("{\"result\": \"OK\", \"content\": \"%s\"}" % routes["api"][self.path], "utf-8"))
        else:
            self.http_header(404, "text/html")
            self.wfile.write(bytes("404: Page not found", "utf-8"))
        return
    
    def do_POST(self):
        self.http_header(200,"text/html")
        length=int(self.headers['length'])
        post_data = self.rfile.read(length)
        userInfo = parser(post_data.decode("UTF-8"))
        if authenticate(userInfo):
            self.wfile.write(bytes("Welcome, " + userInfo["username"], "UTF-8"))
        else:
            self.wfile.write(bytes("Username and password do not match.", "UTF-8"))
        self.wfile.write(bytes("<a href=\"/login\">login</a>", "UTF-8"))
        return
    
    def http_header(self, statuscode, contenttype):
        self.send_response(statuscode)
        self.send_header("Content-type", contenttype)
        self.end_headers()
        
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt: #CTRL + C
        pass

    webServer.server_close()
    print("Server has stopped.")