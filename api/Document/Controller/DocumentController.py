import json

import requests
from Document.Model.Document import Document
from User.Model.User import User
from db import db
from flask import Blueprint, request
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required

document_app = Blueprint(
    "document",
    __name__,
    url_prefix="/api/documents/")


@document_app.route("", methods=["GET"])
@token_required
def get_documents():
    docs = [str(doc) for doc in Document.query.all()]
    return build_response(docs, 200)


@document_app.route("<id>/", methods=["GET"])
@token_required
def get_doc_by_id(id):
    doc = db.get_or_404(Document, id)

    return build_response(str(doc), 200)


@document_app.route("", methods=["POST"])
@token_required
def create_document():
    form = request.get_json()

    doc = Document(
        form['name'],
        form['path'],
        "Created",
        form['user_id']
    )

    db.session.add(doc)
    db.session.commit()

    req_body = {
        'request_type': 'validation',
        'entity_type': 'document',
        'entity_id': doc.id
    }

    response = requests.post("http://localhost:5000/api/requests", json=json.dumps(req_body))

    if response.status_code >= 300:
        return build_response(f"'Failed to create document'", 422)

    return build_response(f"'Created document with id': {doc.id}", 201)


@document_app.route("<id>/", methods=["PUT"])
@token_required
def update_document(id):
    old_doc = db.get_or_404(Document, id)

    form = request.get_json()

    user = db.get_or_404(User, form['user_id'])

    doc = Document(
        form['name'],
        form['path'],
        form['status'],
        form['user_id'],
        user,
        id=old_doc.id,
        created_at=old_doc.created_at
    )

    db.session.delete(old_doc)
    db.session.add(doc)
    db.session.commit()

    req_body = {
        'request_type': 'validation',
        'entity_type': 'document',
        'entity_id': doc.id
    }

    response = requests.post("http://localhost:5000/api/requests", json=req_body)

    if response.status_code >= 300:
        return build_response(f"'Failed to update skill with id': {doc.id}", 422)

    return build_response("{}", 200)


@document_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_document(id):
    doc = db.get_or_404(Document, id)

    db.session.delete(doc)
    db.session.commit()

    return build_response("{}", 200)
