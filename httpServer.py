#!/usr/local/bin/python

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urllib, os, posixpath

class RootedHTTPServer(HTTPServer):

    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path

class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

def runHTTPServer():

    port = 9999
    specify_dir = '/mnt/sdb1/log/'
    print "Serving HTTP on port", port, ", Use double CTRL+C to stop the server."
    server_address = ('', port)
    try:
        httpd = RootedHTTPServer(specify_dir, server_address, RootedHTTPRequestHandler)
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # port already in use
            print("ERROR: The port {0} is already used by another process.".format(port))
        else:
            raise OSError
    except KeyboardInterrupt as interrupt:
        print("Server stopped. Bye bye!")

if __name__ == '__main__':
    runHTTPServer()