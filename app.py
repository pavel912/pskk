from flask import Flask, render_template, request, redirect, url_for, abort
from User import User
from LoginHandler import LoginHandler


app = Flask("App")
loginHandler = LoginHandler()
loginHandler.add_test_users()


@app.get('/')
def index_get():
    return redirect(url_for("login_get"))


@app.get('/login')
def login_get():
    return render_template('login.html')


@app.post('/login')
def login_post():
    user = User(request.form["username"], request.form["password"])
    if loginHandler.login(user):
        return redirect(f"/{user.username}")

    return render_template('login.html', flash_message="Incorrect login or password")


@app.get('/create')
def create_user_get():
    return render_template('create.html')


@app.post('/create')
def create_user_post():
    user = User(request.form["username"], request.form["password"], request.form["email"])
    if not loginHandler.is_user_exists(user):
        loginHandler.create_user(user)
        return redirect(f"/login")

    return render_template('create.html', flash_message="User with this username and password already exists")


@app.get("/<username>")
def user_page_get(username):
    return render_template('userpage.html', username=username)