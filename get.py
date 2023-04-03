from http.server import *
import json
from post import *


class PostClass(UserClass):

    def do_GET(self):
        if self.path == '/getPost' and self.command == 'GET':

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
                            posts = Post(user_id=user_id).all()
                            post_list = []
                            for post in posts:
                                post_dict = {
                                    'id': str(post.id),
                                    'user_id': post.user_id,
                                    'title': post.title,
                                    'body': post.body,
                                    'created_at': str(post.created_at),
                                }
                                post_list.append(post_dict)
                            self.send_response(200)
                            self.send_header('Content-Type',
                                             'application/json')
                            self.end_headers()
                            response = json.dumps(post_list)
                            self.wfile.write(response.encode())
                        else:
                            raise Exception("no post created at.")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_message = str(e)
                self.wfile.write(json.dumps({"error": error_message}).encode())