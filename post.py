from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from mongoengine import *
from authenticate import verify_token, is_authenticated
import jwt

from modles import db_disconnect, db_connection, User, Post, Vote, Admin
import modles


class UserClass(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/createAccount' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)

            try:
                if data["email"] == "" or data["password"] == "" or data[
                        "first_name"] == "" or data["last_name"] == "" or data[
                            "password"] == "" or data[
                                "confirm_password"] == "" or data["phone"] < 10:
                    raise Exception("Fields can not be empty")
                if data["password"] != data["confirm_password"]:
                    raise Exception(
                        "Password and confirm password fields do not match.")
                db_disconnect()
                db_connection()
                user = User(email=data["email"],
                            first_name=data["first_name"],
                            last_name=data["last_name"],
                            phone=data["phone"])
                user.set_password(data["password"])
                user.save()
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "User created successfully"}
                self.wfile.write(json.dumps(response).encode())

            except NotUniqueError as e:
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "User already exists"}
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())

        elif self.path == '/login' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            try:
                if data["email"] == "" or data["password"] == "":
                    raise Exception("Fields can not be empty")
                db_disconnect()
                db_connection()
                user = User.objects(email=data["email"]).first()
                if user:

                    if User.check_password(user, data["password"]):
                        # Generate a JWT containing the user ID and a secret key
                        payload = {'user_id': str(user.id)}
                        secret_key = 'mysecret'
                        token = jwt.encode(payload,
                                           secret_key,
                                           algorithm='HS256')
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {
                            "message": "User authenticated successfully",
                            "token": token
                        }
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        raise Exception("Invalid email or password")
                else:
                    raise Exception("No user data is available")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_message = str(e)
                self.wfile.write(json.dumps({"error": error_message}).encode())

        elif self.path == '/createPost' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            try:
                if not is_authenticated(self):
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {"error": "User is not loggedin."}
                    self.wfile.write(json.dumps(response).encode())

                else:
                    token = self.headers.get("Authorization")
                    if not verify_token(token):
                        self.send_response(401)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {"error": "Invalid token"}
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        decoded_token = jwt.decode(token,
                                                   'mysecret',
                                                   algorithms=['HS256'])
                        user_id = decoded_token['user_id']
                        db_disconnect()
                        db_connection()
                        user = User.objects(id=user_id).first()
                        if user:
                            post = Post(user_id=str(user.id),
                                        title=data["title"],
                                        body=data["body"])
                            post.save()
                            self.send_response(201)
                            self.send_header('Content-Type',
                                             'application/json')
                            self.end_headers()
                            response = {"message": "Post created successfully"}
                            self.wfile.write(json.dumps(response).encode())
                        else:
                            raise Exception("No user data is available")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_message = str(e)
                self.wfile.write(json.dumps({"error": error_message}).encode())

        elif self.path == '/votePost' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            vote_data = json.loads(body)

            try:
                if not is_authenticated(self):
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {"error": "User is not loggedin."}
                    self.wfile.write(json.dumps(response).encode())

                else:
                    token = self.headers.get("Authorization")
                    if not verify_token(token):
                        self.send_response(401)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {"error": "Invalid token"}
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        decoded_token = jwt.decode(token,
                                                   'mysecret',
                                                   algorithms=['HS256'])
                        user_id = decoded_token['user_id']
                        db_disconnect()
                        db_connection()
                        user = User.objects(id=user_id).first()

                        if user:
                            votes = Vote.objects(post_id=vote_data["post_id"],
                                                 user_id=str(user.id))
                            if votes:
                                raise Exception(
                                    "User already voted on this post.")
                            vote1 = Vote(user_id=str(user.id),
                                         post_id=vote_data["post_id"],
                                         vote=vote_data["vote"])
                            vote1.save()
                            self.send_response(201)
                            self.send_header('Content-Type',
                                             'application/json')
                            self.end_headers()
                            response = {"message": "Voted"}
                            self.wfile.write(json.dumps(response).encode())
                        else:
                            raise Exception("No user data is available")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_message = str(e)
                self.wfile.write(json.dumps({"error": error_message}).encode())

        elif self.path == '/createAdmin' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)

            try:
                if data["email"] == "" or data["password"] == "" or data[
                        "first_name"] == "" or data["last_name"] == "" or data[
                            "password"] == "" or data[
                                "confirm_password"] == "" or data["phone"] < 10:
                    raise Exception("Fields can not be empty")
                if data["password"] != data["confirm_password"]:
                    raise Exception(
                        "Password and confirm password fields do not match.")
                db_disconnect()
                db_connection()
                admin = Admin(email=data["email"],
                              first_name=data["first_name"],
                              last_name=data["last_name"],
                              phone=data["phone"])
                admin.set_password(data["password"])
                admin.save()
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "Admin created successfully"}
                self.wfile.write(json.dumps(response).encode())

            except NotUniqueError as e:
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"message": "Admin already exists"}
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())