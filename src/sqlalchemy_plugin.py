#
# The plugin of sqlalchemy DB. Started when bus start...
#
import cherrypy
import logging

from cherrypy.process import plugins
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from contextlib import contextmanager


class SAPlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus registery.

        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.
        """

        super().__init__(bus)

        self.engine = None
        self.Session = None
        self.Base = None
        self.db_uri = None

        self.temp_connection = None

    def use_sqlite(self, location=":memory:"):
        if self.engine is not None:
            raise "Database is already started"

        self.db_uri = "sqlite:///" + location

    def connect_database(self):
        self.bus.log('Starting up DB access')

        if self.db_uri is None:
            raise "Database string is not define"

        self.engine = create_engine(self.db_uri, echo=False,
                                    connect_args={'check_same_thread': False},
                                    poolclass=StaticPool)

        try:
            self.Base.metadata.create_all(self.engine)
        except OperationalError:
            print("-" * 20)
            print("Can't connect " + self.db_uri)
            print("-" * 20)

            cherrypy.engine.exit()
            exit()

        self.Session = sessionmaker(bind=self.engine)

    def start(self):
        pass

    @contextmanager
    def session_scope(self, **parameters):
        if self.temp_connection is not None:
            session = self.temp_connection
            self.temp_connection = None
        else:
            session = self.Session(**parameters)

        try:
            yield session
            session.commit()
            session.close()

        except Exception as e:
            session.rollback()
            session.close()
            raise e

    def start_connection(self, **parameters):
        if self.temp_connection is None:
            self.temp_connection = self.Session(**parameters)

        return self.temp_connection

    def close_connection(self):
        if self.temp_connection is None:
            return

        try:
            self.temp_connection.commit()
            self.temp_connection.close()
            self.temp_connection = None

        except Exception as e:
            self.temp_connection.rollback()
            self.temp_connection.close()
            self.temp_connection = None
            raise e

    def stop(self):
        self.bus.log('Stopping down DB access')
        if self.engine:
            self.engine.dispose()
            self.engine = None


class SATool(cherrypy.Tool):
    def __init__(self, sa_plugin):
        """
        The SA tool is responsible for associating a SA session
        to the SA engine and attaching it to the current request.
        Since we are running in a multithreaded application,
        we use the scoped_session that will create a session
        on a per thread basis so that you don't worry about
        concurrency on the session object itself.

        This tools binds a session to the engine each time
        a requests star,ts and commits/rollbacks whenever
        the request terminates.
        """

        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_connection,
                               priority=10)
        self.sa_plugin = sa_plugin

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_request',
                                      self.close_connection,
                                      priority=80)

    def get_plugin(self):
        return self.sa_plugin

    def bind_connection(self):
        """
        Attaches a session to the request's scope by requesting
        the SA plugin to bind a session to the SA engine.
        """
        cherrypy.request.db = self.sa_plugin

    def close_connection(self):
        """
        Commits the current transaction or rolls back
        if an error occurs. Removes the session handle
        from the request's scope.
        """
        if not hasattr(cherrypy.request, 'db'):
            return

        cherrypy.request.db.close_connection()  # close the db connection
