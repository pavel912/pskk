import os

from flask import Blueprint, request
from db import db
from api.Request.Model.Request import Request
from utils.SessionsUtils import build_response

request_app = Blueprint(
    "request",
    __name__,
    url_prefix="/api/requests")


@request_app.route("/", methods=["GET"])
def get_all_requests():
    requests = [str(req) for req in Request.query().all()]

    return build_response(requests, 200)


@request_app.route("/<id>", methods=["GET"])
def get_request_by_id(id):
    req = db.get_or_404(Request, id)

    return build_response(str(req), 200)


# not implemented
@request_app.route("/", methods=["POST"])
def create_request():
    req = Request(
        request.json["type"],
        request.json["status"]
    )

    db.session.add(req)
    db.session.commit()

    return build_response(f"'Created request with id': {req.id}", 201)


# not implemented
@request_app.route("/<id>", methods=["PUT"])
def update_request(id):
    old_req = db.get_or_404(Request, id)

    req = Request(
        request.json["type"],
        request.json["status"],
        id=old_req.id,
        created_at=old_req.created_at
    )

    db.session.delete(old_req)
    db.session.add(req)
    db.session.commit()

    return build_response("{}", 200)


# not implemented
@request_app.route("/<id>", methods=["DELETE"])
def delete_request(id):
    req = db.get_or_404(Request, id)

    db.session.delete(req)
    db.session.commit()

    return build_response("{}", 200)
