import cherrypy

from .rest_api import MainRestViewHandler


class ViewHandler:
    pass

class MainViewHandler(ViewHandler):
    def __init__(self):
        self.rest = MainRestViewHandler()

    @cherrypy.expose
    def index(self, **kwargs):
        return "Index"
