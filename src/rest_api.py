import cherrypy
import logging

# from .view_utilities import Keys

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


class HTTPError(Exception):
    def __init__(self, status=400, msg=""):
        super().__init__()
        self.status = status
        self.msg = msg


def jsonlize_response(func):
    def wrapper(*args, **kwargs):
        result = None
        try:
            method = cherrypy.request.method

            if method == GET or method == DELETE:
                data = kwargs
            elif method == POST or method == PUT:
                data = cherrypy.request.json
            else:
                data = {}

            result = func(args[0], method, args[1:], data)
            if result is None:
                result = {}
            if "success" not in result:
                result["success"] = True

        except HTTPError as e:
            cherrypy.response.status = e.status
            result = {
                "success": False,
                "status_code": e.status,
                "reason": e.msg,
            }

            if e.status == 404:
                result["reason"] = "Page not found"

        except:
            logging.exception("Caught server error")
            result = {
                "success": False,
                "status_code": 500,
                "reason": "Server unexpected error"
            }
            cherrypy.response.status = 500

        return result

    return wrapper


class ResetViewHandler:
    _cp_config = {
        "tools.json_out.on": True,
        "tools.json_in.on": True,
        # "tools.dbtool.on": True,
        # "tools.keytool.on": True,
        "tools.encode.on": True,
    }


class MainRestViewHandler(ResetViewHandler):
    def __init__(self):
        pass

    @cherrypy.expose
    @jsonlize_response
    def index(self, method, args, data):
        print(method, args, data)
        return {"msg": "You in the passage of the 'REST'"}
