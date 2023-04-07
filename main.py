import os
import datetime
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

application = Flask(__name__)
# Define secret key for our application to protect against malicious actions.

# TODO: DEFINE SECRET KEY AS ENVIRONMENT VARIABLE
application.config["SECRET_KEY"] = os.getenv("flask_secret_key")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 465
application.config["MAIL_USE_SSL"] = True
application.config["MAIL_PASSWORD"] = os.getenv("work_application")
application.config["MAIL_USERNAME"] = "kyligalway@gmail.com"

database = SQLAlchemy(application)
mail = Mail(application)


class Form(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(80))
    last_name = database.Column(database.String(80))
    email = database.Column(database.String(80))
    start_date = database.Column(database.Date)
    occupation = database.Column(database.String(80))


@application.route("/", methods=["GET"])
def getIndex():
    message = flask.session["message"] if "message" in flask.session and flask.session["message"] is not None else None
    return flask.render_template("index.html", message=message)


@application.route("/submitForm", methods=["POST"])
def submitForm():
    first_name = flask.request.form["first_name"]
    last_name = flask.request.form["last_name"]
    print(flask.request.form["start_date"])
    start_date = datetime.datetime.strptime(flask.request.form["start_date"], "%Y-%m-%d")
    print(type(start_date))
    email = flask.request.form["email"]
    occupation = flask.request.form["current_occupation"]

    job_form_submit = Form(first_name=first_name, last_name=last_name, start_date=start_date, email=email,
                           occupation=occupation)
    database.session.add(job_form_submit)
    database.session.commit()

    message_body = f"""Thank you for your application, {first_name} {last_name}!
You will hear from us soon!
Application Data: 
    Name: {first_name} {last_name}
    Email: {email}
    Start Date: {start_date.__str__()}
    Current Occupation: {occupation}
"""
    print(message_body)

    message = Message(subject="New Work Application", sender=application.config["MAIL_USERNAME"],
                      recipients=[email], body=message_body)
    mail.send(message)

    flask.session["message"] = f"Thank you for applying {first_name} {last_name}!"

    return flask.redirect("/")


if __name__ == "__main__":
    with application.app_context():
        database.create_all()
        application.run(debug=True, port=5001)

# This opens up a port on our computer to use as a web server. When we send a request through the browser, it will
# route the request through one of the routes we specify in our application to return a formatted html page as response.
