from flask import Flask, render_template, request, redirect, url_for, abort, make_response
from User import User
from LoginHandler import LoginHandler
from DataValidator import DataValidator

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
    user = loginHandler.get_user_by_username_and_password(User(request.form["username"], request.form["password"]))
    if not user:
        return make_response(render_template('login.html', flash_message="Incorrect login or password"), 401)

    return redirect(f"/user/id/{user.id}")


@app.get('/create')
def create_user_get():
    return render_template('create.html')


@app.post('/create')
def create_user_post():
    validator = DataValidator()

    user_data = User(request.form["username"],
        request.form["password"],
        request.form["email"],
        request.form["name"],
        request.form["surname"],
        request.form["fathers_name"],
        validator.convert_string_to_date(request.form["date_of_birth"]),
        request.form["job_role"],
        request.form["company_name"])

    error_messages = validator.validate_user_data(user_data)

    user = loginHandler.get_user_by_username_and_password(user_data)

    if user:
        error_messages.append("User with this username and password already exists")
    elif request.form["password"] != request.form["confirm_password"]:
        error_messages.append("Passwords do not match")

    if error_messages:
        return make_response(render_template('create.html', error_messages=error_messages, user_data=user_data), 401)

    loginHandler.create_user(user_data)
    return redirect("/login")


@app.get("/user/id/<id>")
def user_page_get(id):
    return render_template('userpage.html', user=loginHandler.get_user_by_id(id))

@app.get("/user/id/<id>/update_data")
def update_user_data_get(id):
    return render_template('update_data.html', user_data=loginHandler.get_user_by_id(id))

@app.post("/user/id/<id>/update_data")
def update_user_data_post(id):
    validator = DataValidator()

    user = loginHandler.get_user_by_id(id)

    user.update_data(
        request.form["username"],
        request.form["email"],
        request.form["name"],
        request.form["surname"],
        request.form["fathers_name"],
        validator.convert_string_to_date(request.form["date_of_birth"]),
        request.form["job_role"],
        request.form["company_name"])

    error_messages = validator.validate_user_data(user)

    if not user:
        error_messages.append("User with this username and password does not exist")

    if error_messages:
        return make_response(render_template('update_data.html', error_messages=error_messages, user_data=user), 401)

    loginHandler.update_user(user)
    return redirect(f"/user/id/{user.id}")

@app.get("/user/id/<id>/update_password")
def update_user_password_get(id):
    return render_template('update_password.html', user_data=loginHandler.get_user_by_id(id))

@app.post("/user/id/<id>/update_password")
def update_user_password_post(id):
    validator = DataValidator()

    user = loginHandler.get_user_by_id(id)

    if not user:
        error_messages.append("User with this username and password does not exist")
    elif request.form["password"] != user.password:
        print(request.form["password"], user.password)
        error_messages.append("Incorrect password")
    elif request.form["new_password"] != request.form["confirm_password"]:
        error_messages.append("Passwords do not match")

    user.update_password(
        request.form["new_password"])

    error_messages = validator.validate_user_data(user)

    if error_messages:
        return make_response(render_template('update_password.html', error_messages=error_messages, user_data=user), 401)

    loginHandler.update_user(user)
    return redirect(f"/user/id/{user.id}")