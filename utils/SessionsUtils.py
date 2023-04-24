from flask import render_template, request, redirect, make_response, session


def is_exists_user_session(id: str):
    if "user_id" not in session:
        return False

    return session["user_id"] == int(id)
