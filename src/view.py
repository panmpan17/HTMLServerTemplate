import cherrypy


class ViewHandler:
    pass

class MainViewHandler(ViewHandler):
    @cherrypy.expose
    def index(self, ):
        return "Index"
