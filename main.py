import json
from flask import escape
from local.model import SetModel

def processRequest(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'deck' in request_json:
        deck = request_json['deck']
    elif request_args and 'deck' in request_args:
        deck = request_args['deck']
    else:
        return json.dumps({"error":"Missing 'dec' key"})
    deck = json.loads(deck)
    solution = SetModel.SolveFromRequest(deck)
    return (json.dumps(solution), 200, headers)
