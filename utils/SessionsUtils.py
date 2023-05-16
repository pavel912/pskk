import datetime

from flask import render_template, request, redirect, make_response, session


def is_exists_user_session(id: str):
    if "user_id" not in session:
        return False

    return session["user_id"] == int(id)


def is_admin():
    if "role" not in session:
        return False

    return session["role"] == "Admin"


def to_json(obj):
    representation = vars(obj)
    if '_sa_instance_state' in representation:
        representation.pop('_sa_instance_state')

    if 'password' in representation:
        representation.pop('password')

    for key in representation:
        if type(representation[key]) == list:
            representation[key] = [sub_obj.id for sub_obj in representation[key]]

        if type(representation[key]) == datetime.datetime or type(representation[key]) == datetime.date:
            representation[key] = str(representation[key])

    return str(representation)


def build_response(body, code):
    response = make_response(body, code)
    response.headers['Content-Type'] = 'application/json'
    return response
