import os
import datetime
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
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None else None
    return flask.render_template("/index.html", message=message)


@application.route("/submitApplication", methods=["GET"])
def getSubmitApplication():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None else None
    return flask.render_template("/submit_application.html", message=message)


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

    flask.session["message"] = f"Thank you for applying {first_name} {last_name}!"
    return flask.redirect("/submitApplication")


@application.route("/viewApplications", methods=["GET"])
def getViewApplications():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None else None
    applications = repository.select_applications()

    return flask.render_template("admin/view_applications.html", message=message, applications=applications)


@application.route("/addUser", methods=["GET"])
def getAddUser():
    message = flask.session.pop("message") if "message" in flask.session and flask.session["message"] is not None else None
    return flask.render_template("/admin/add_user.html", message=message)


if __name__ == "__main__":
    with application.app_context():
        application.run(debug=True, port=5001)
