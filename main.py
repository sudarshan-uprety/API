from http.server import *
from get import *
from post import *
from delete import *

httpd = HTTPServer(('localhost', 4000), DeleteClass)
httpd.serve_forever()