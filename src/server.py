import cherrypy
import os

from .view import MainViewHandler


class Server:
    RENDER_CONFIG = {
        "/static": {
            "tools.staticdir.root": os.path.join(
                os.path.dirname(__file__), "static"),
            "tools.staticdir.on": True,
            "tools.staticdir.dir": ".",
        }
    }

    def __init__(self):
        pass
    
    def run(self):
        cherrypy.quickstart(MainViewHandler(), "/", self.RENDER_CONFIG)
