from flask import Response

class MyResponse(Response):
    default_mimetype = "application/xml"