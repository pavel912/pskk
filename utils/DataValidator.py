from api.User.Model.User import User
import re
import datetime as dt

string_pattern = re.compile("[a-zA-Z0-9]+")
email_pattern = re.compile("[a-zA-Z0-9]+@([a-z]{3,}.)+[a-z]{2,}")


def validate_user_data(user: User) -> list:
    error_messages = []
    if not validate_string(user.username):
        error_messages.append("Username should contain only lower and upper case latin letters and numbers")
    if not validate_string(user.company_name):
        error_messages.append("Company name should contain only lower and upper case latin letters and numbers")
    if not validate_string(user.name):
        error_messages.append("Name should contain only lower and upper case latin letters and numbers")
    if not validate_string(user.surname):
        error_messages.append("Surname should contain only lower and upper case latin letters and numbers")
    if not validate_string(user.fathers_name):
        error_messages.append("Father's name should contain only lower and upper case latin letters and numbers")
    if not validate_string(user.job_role):
        error_messages.append("Job role should contain only lower and upper case latin letters and numbers")
    if not validate_password(user.password):
        error_messages.append(
            "Password should contain at least one upper case letter, number and special simvols except for '.', ';' and ','")
    if not validate_email(user.email):
        error_messages.append(
            "Email's mail part should contain at least three lower case latin letters and domain should contain at least two")
    if not validate_birthdate(user.date_of_birth):
        error_messages.append("Birth date could not be in the future")

    return error_messages


def validate_birthdate(date: dt.date) -> bool:
    return dt.datetime.now().date() > date


def convert_string_to_date(date: str) -> dt.date:
    return dt.date.fromisoformat(date) if len(date) > 0 else dt.date(1, 1, 1)


def validate_password(password: str) -> bool:
    return validate_string(password)


def validate_email(email: str) -> bool:
    return bool(email_pattern.fullmatch(email))


def validate_string(data: str) -> bool:
    if len(data) > 0:
        return bool(string_pattern.fullmatch(data))

    return True
