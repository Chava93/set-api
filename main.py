import json
from flask import escape
from local.model import SetModel

def processRequest(request):
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
    return json.dumps(solution)
