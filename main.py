from http.server import *
from get import *
from post import *


httpd = HTTPServer(('localhost', 4000),PostClass)
httpd.serve_forever()



