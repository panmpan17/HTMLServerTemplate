import cherrypy
import os
import jinja2

from datetime import datetime
from .rest_api import MainRestViewHandler


TIMESTAMP = str(int(datetime.now().timestamp()))


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), "templates")))


class ViewHandler:
    @staticmethod
    def render_html(html_file, **params):
        t = jinja_env.get_template(html_file)
        return t.render(params)

class MainViewHandler(ViewHandler):
    def __init__(self):
        self.rest = MainRestViewHandler()

    @cherrypy.expose
    def index(self, **kwargs):
        return self.render_html("index.html")

    @cherrypy.expose
    def timestamp(self, **kwargs):
        """
        Return the time stamp when the server starts.
        Use in loading newest static files
        """
        return TIMESTAMP
