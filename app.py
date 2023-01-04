from flask import Flask, render_template, request, redirect, url_for, make_response, abort, session
from entities.User import User
from utils.DB_Handler import DB_Handler
from utils.Data_Validator import Data_Validator

app = Flask("App")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # replace it letter for safety issues

DB_Handler = DB_Handler()
DB_Handler.add_test_users()


@app.get('/')
def index_get():
    return redirect(url_for("login_get"))


@app.get('/login')
def login_get():
    return render_template('login.html')


@app.post('/login')
def login_post():
    user = DB_Handler.get_user_by_username_and_password(User(request.form["username"], request.form["password"]))
    if not user:
        return make_response(render_template('login.html', flash_message="Incorrect login or password"), 401)

    session['user_id'] = user.id
    return redirect(f"/user/id/{user.id}")


@app.get('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.get('/create')
def create_user_get():
    return render_template('create.html')


@app.post('/create')
def create_user_post():
    error_messages = []
    
    validator = Data_Validator()

    if not DB_Handler.is_unique_username(request.form["username"]) or not DB_Handler.is_unique_password(request.form["password"]):
        error_messages.append("User with this username or password already exists")
    elif request.form["password"] != request.form["confirm_password"]:
        error_messages.append("Passwords do not match")
    
    user_data = User(request.form["username"],
        request.form["password"],
        request.form["email"],
        request.form["name"],
        request.form["surname"],
        request.form["fathers_name"],
        validator.convert_string_to_date(request.form["date_of_birth"]),
        request.form["job_role"],
        request.form["company_name"])

    error_messages += validator.validate_user_data(user_data)

    if error_messages:
        return make_response(render_template('create.html', error_messages=error_messages, user_data=user_data), 401)

    DB_Handler.create_user(user_data)
    return redirect("/login")


@app.get("/user/id/<id>")
def user_page_get(id):
    user = DB_Handler.get_user_by_id(id)

    if not user:
        abort(404)
    
    if ("user_id" not in session) | (session["user_id"] != user.id):
        return redirect("/login")

    return render_template('userpage.html', user=user)

@app.get("/user/id/<id>/update_data")
def update_user_data_get(id):
    user = DB_Handler.get_user_by_id(id)

    if not user:
        abort(404)

    if ("user_id" not in session) | (session["user_id"] != user.id):
        return redirect("/login")
    
    return render_template('update_data.html', user_data=user)

@app.post("/user/id/<id>/update_data")
def update_user_data_post(id):
    error_messages = []

    validator = Data_Validator()

    user = DB_Handler.get_user_by_id(id)

    if not user:
        abort(404)

    if ("user_id" not in session) | (session["user_id"] != user.id):
        abort(404)

    if not user:
        error_messages.append("User with this username and password does not exist")
    elif not DB_Handler.is_unique_username(request.form["username"]):
        error_messages.append("User with this username already exists")
    
    user.update_data(
        request.form["username"],
        request.form["email"],
        request.form["name"],
        request.form["surname"],
        request.form["fathers_name"],
        validator.convert_string_to_date(request.form["date_of_birth"]),
        request.form["job_role"],
        request.form["company_name"])

    error_messages += validator.validate_user_data(user)

    if error_messages:
        return make_response(render_template('update_data.html', error_messages=error_messages, user_data=user), 401)

    DB_Handler.update_user(user)
    return redirect(f"/user/id/{user.id}")

@app.get("/user/id/<id>/update_password")
def update_user_password_get(id):
    user = DB_Handler.get_user_by_id(id)

    if not user:
        abort(404)

    if ("user_id" not in session) | (session["user_id"] != user.id):
        return redirect("/login")

    return render_template('update_password.html', user_data=user)

@app.post("/user/id/<id>/update_password")
def update_user_password_post(id):
    error_messages = []

    validator = Data_Validator()

    user = DB_Handler.get_user_by_id(id)

    if not user:
        abort(404)

    if ("user_id" not in session) | (session["user_id"] != user.id):
        abort(404)

    if not user:
        error_messages.append("User with this username and password does not exist")
    elif request.form["password"] != user.password:
        error_messages.append("Incorrect password")
    elif not DB_Handler.is_unique_password(request.form["new_password"]):
        error_messages.append("User with this password already exists")
    elif request.form["new_password"] != request.form["confirm_password"]:
        error_messages.append("Passwords do not match")
    

    user.update_password(
        request.form["new_password"])

    error_messages += validator.validate_user_data(user)

    if error_messages:
        return make_response(render_template('update_password.html', error_messages=error_messages, user_data=user), 401)

    DB_Handler.update_user(user)
    return redirect(f"/user/id/{user.id}")