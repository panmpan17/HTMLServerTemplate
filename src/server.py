import sqlalchemy
from sqlalchemy import sql
import cherrypy
import os

from .view import MainViewHandler
from .model import Base
from .sqlalchemy_plugin import SAPlugin, SATool


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
        sqlalchemy_plugin = SAPlugin(cherrypy.engine)
        sqlalchemy_plugin.use_sqlite("test.db")
        sqlalchemy_plugin.Base = Base
        sqlalchemy_plugin.connect_database()
        sqlalchemy_plugin.subscribe()

        cherrypy.tools.database = SATool(sqlalchemy_plugin)

    def run(self):
        cherrypy.quickstart(MainViewHandler(), "/", self.RENDER_CONFIG)
