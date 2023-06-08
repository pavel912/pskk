import json
from flask import make_response

def to_json(obj):
    representation = vars(obj)
    repr_dict = dict()
    for key in representation:
        if key in ('_sa_instance_state', 'password'):
            continue

        if type(representation[key]) == list:
            repr_dict[key] = [sub_obj.id for sub_obj in representation[key]]
        # elif type(representation[key]) == datetime.datetime or type(representation[key]) == datetime.date:
        #    representation[key] = str(representation[key])
        else:
            repr_dict[key] = str(representation[key])

    return json.dumps(repr_dict)


def build_response(body, code):
    response = make_response(body, code)
    response.headers['Content-Type'] = 'application/json'
    return response
