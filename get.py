from http.server import *
import json
from post import *

class PostClass(UserClass):

    def do_GET(self):
        if self.path=='/createPost' and self.command=='GET':
            pass