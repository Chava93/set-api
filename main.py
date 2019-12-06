from flask import escape
from local.model import SetModel

def processRequest(request):
    request_json = request.get_json(silent=True)
    return request_json
