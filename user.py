from http.server import HTTPServer, BaseHTTPRequestHandler 
import json 

from modles import connect,disconnect,User


class UserFunctions(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path=='/create' and self.command=='POST':
            content_length=int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data=json.loads(body)
            if data["email"] == "" or data["password"] == "" or data["first_name"]=="" or data["last_name"]=="" or data["password"]=="":
                self.send_error(400,"Fields can not be empty")
            # disconnect(alias='default')
            # connect()
            # user=User(email=data["email"],first_name=data["first_name"],last_name=data["last_name"],password=data["password"])
            # user.save()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"message": "User created successfully"}
            self.wfile.write(json.dumps(response).encode())

    
httpd = HTTPServer(('localhost', 4000), UserFunctions) 
httpd.serve_forever()