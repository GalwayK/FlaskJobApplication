import os
import datetime
import bcrypt
import flask
from flask import Flask
import emailing
import repository

application = Flask(__name__)

application.config["SECRET_KEY"] = os.getenv("flask_secret_key")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 465
application.config["MAIL_USE_SSL"] = True
application.config["MAIL_PASSWORD"] = os.getenv("work_application")
application.config["MAIL_USERNAME"] = "kyligalway@gmail.com"


@application.route("/", methods=["GET"])
def getIndex():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None \
        else None
    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None

    return flask.render_template("/index.html", message=message, account=account)


@application.route("/submitApplication", methods=["GET"])
def getSubmitApplication():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None \
        else None

    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None

    if account and ("Admin" in account["roles"] or "User" in account["roles"]):
        return flask.render_template("/submit_application.html", message=message, account=account)
    else:
        return flask.redirect("/forbidden")


@application.route("/submitApplication", methods=["POST"])
def postSubmitApplication():
    first_name = flask.request.form["first_name"]
    last_name = flask.request.form["last_name"]
    print(flask.request.form["start_date"])
    start_date = datetime.datetime.strptime(flask.request.form["start_date"], "%Y-%m-%d")
    email = flask.request.form["email"]
    occupation = flask.request.form["current_occupation"]

    repository.insert_application(first_name, last_name, email, start_date, occupation)

    emailing.send_application_email(first_name, last_name, email, start_date, occupation)

    flask.session["message"] = f"<p id = 'success_message'> Thank you for applying {first_name} {last_name}! </p>"
    return flask.redirect("/submitApplication")


@application.route("/viewApplications", methods=["GET"])
def getViewApplications():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None \
        else None

    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None

    if account and "Admin" in account["roles"]:
        applications = repository.select_applications()

        return flask.render_template("admin/view_applications.html", message=message, applications=applications,
                                     account=account)
    else:
        return flask.redirect("/forbidden")


@application.route("/addUser", methods=["GET"])
def getAddUser():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None \
        else None

    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None

    if account and "Admin" in account["roles"]:
        return flask.render_template("/admin/add_user.html", message=message, roles=["Admin", "User"], account=account)
    else:
        return flask.redirect("/forbidden")


@application.route("/addUser", methods=["POST"])
def postAddUser():
    account_name = flask.request.form["account_name"]
    password_one = flask.request.form["passwordOne"]
    password_two = flask.request.form["passwordTwo"]
    list_roles = flask.request.form["list_roles"].split(",")
    print(account_name)
    print(password_one)
    print(password_two)
    print(list_roles)

    error_code = 0
    if password_two == password_one:
        error_code = repository.insert_account(account_name, password_one, list_roles)

    flask.session["message"] = f"<p id = 'success_message'> Successfully added account {account_name}! </p>" \
        if error_code == 1 else f"<p id = 'fail_message'> Error adding account {account_name}! </p>"

    return flask.redirect("/addUser")


@application.route("/signIn", methods=["GET"])
def getSignIn():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None \
        else None

    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None

    return flask.render_template("sign_in.html", message=message, account=account)


@application.route("/signIn", methods=["POST"])
def postSignIn():
    str_password = flask.request.form["password"]
    str_username = flask.request.form["username"]

    fetched_account = repository.select_account_by_account_name(str_username)
    bool_match = bcrypt.checkpw(str_password.encode("utf-8"), fetched_account[2])
    flask.session["message"] = f"<p id = 'success_message'> Successfully signed in account {str_username}! </p>" \
        if bool_match else f"<p id = 'fail_message'> Error signing into account {str_username}! </p>"

    if bool_match:
        new_user = {"username": fetched_account[1]}
        account_roles = repository.read_role_id_by_account_id(fetched_account[0])
        new_user["roles"] = []
        for account_role in account_roles:
            new_user["roles"].append(repository.read_role_name_by_role_id(account_role[1]))
        print(new_user)
        flask.session["current_user"] = new_user
        return flask.redirect("/")

    else:
        return flask.redirect("/signIn")


@application.route("/signOut", methods=["GET"])
def getSignOut():
    account = flask.session.get("current_user") if "current_user" in flask.session and flask.session["current_user"] \
                                                   is not None else None
    if account:
        str_username = account['username']
        flask.session["current_user"] = None
        message = f"<p class = neutral-message> User {str_username} signed out </p>"
        flask.session["message"] = message
    else:
        message = f"<p class = neutral-message> No account currently signed in </p>"
        flask.session["message"] = message

    return flask.redirect("/")


@application.route("/forbidden", methods=["GET"])
def getForbidden():
    return flask.render_template("forbidden.html")


@application.errorhandler(404)
def getError(error):
    return flask.render_template("error.html")


if __name__ == "__main__":
    with application.app_context():
        application.run(debug=True, port=5001)
