from http.server import HTTPServer, BaseHTTPRequestHandler 
import json 
from mongoengine import *

from modles import db_disconnect,db_connection,User
import modles


class UserFunctions(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path=='/create' and self.command=='POST':
            content_length=int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data=json.loads(body)

            try:
                if data["email"] == "" or data["password"] == "" or data["first_name"]=="" or data["last_name"]=="" or data["password"]=="" or data["confirm_password"]=="" or data["phone"]<10:
                    raise Exception("Fields can not be empty")
                if data["password"]!=data["confirm_password"]:
                    raise Exception("Password and confirm password fields do not match.")
                db_disconnect()
                db_connection()
                user=User(email=data["email"],first_name=data["first_name"],last_name=data["last_name"],phone=data["phone"])
                user.set_password(data["password"])
                user.save()
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "User created successfully"}
                self.wfile.write(json.dumps(response).encode())


            except NotUniqueError as e:
                print(e)
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "User already exists"}
                self.wfile.write(json.dumps(response).encode())


            except Exception as e:
                print(e)
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())
                
        if self.path=='/login' and self.command=='POST':
            content_length=int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data=json.loads(body)
            try:
                if data["email"]=="" or data["password"]=="":
                    raise Exception("Fields can not be empty")
                db_disconnect()
                db_connection()
                user = User.objects(email=data["email"]).first()
                if user:
                    
                    if modles.User.check_password(user,data["password"]):
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {"message": "User authenticated successfully"}
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        raise Exception("Invalid email or password")
                else:
                    raise Exception("No user data is available")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_message=str(e)
                self.wfile.write(json.dumps({"error": error_message}).encode())



    
httpd = HTTPServer(('localhost', 4000), UserFunctions) 
httpd.serve_forever()