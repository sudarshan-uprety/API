from http.server import *
import json
from post import *
from get import *


class DeleteClass(PostClass):

    def do_DELETE(self):
        if self.path == '/deletePost' and self.command == 'DELETE':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)

            try:
                if not is_authenticated(self):
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {
                        "error": "User is not loggedin to delete a post."
                    }
                    self.wfile.write(json.dumps(response).encode())

                else:
                    token = self.headers.get('Authorization')
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
                            post_id = data.get("post_id")
                            if post_id:
                                post = Post.objects(id=post_id).first()
                                if post and post.user_id == user_id:
                                    post.delete()
                                    self.send_response(200)
                                    self.send_header('Content-Type',
                                                     'application/json')
                                    self.end_headers()
                                    response = {
                                        "message": "Post deleted successfully"
                                    }
                                    self.wfile.write(
                                        json.dumps(response).encode())

                                elif not post:
                                    self.send_response(404)
                                    self.send_header('Content-Type',
                                                     'application/json')
                                    self.end_headers()
                                    response = {"error": "No post found."}
                                    self.wfile.write(
                                        json.dumps(response).encode())

                                else:
                                    self.send_response(401)
                                    self.send_header('Content-Type',
                                                     'application/json')
                                    self.end_headers()
                                    response = {
                                        "error":
                                        "User is not authorized to delete this post."
                                    }
                                    self.wfile.write(
                                        json.dumps(response).encode())

                            else:
                                self.send_response(400)
                                self.send_header('Content-Type',
                                                 'application/json')
                                self.end_headers()
                                response = {
                                    "error": "Missing post_id parameter"
                                }
                                self.wfile.write(json.dumps(response).encode())
                        else:
                            self.send_response(401)
                            self.send_header('Content-Type',
                                             'application/json')
                            self.end_headers()
                            response = {"error": "User not found"}
                            self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())