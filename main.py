# If we have static web elements such as images or JavaScript scripts, we put them inside
# the static folder.
import flask

application = flask.Flask(__name__)

# In between the application declaration and the run line, we put in our mappings
# to handle all http requests which we receive with our application. When
# we receive a http request, we will return a generated webpage in response.


@application.route("/job-request")
def get_index():
    return flask.render_template("index.html")


application.run(debug=True, port=5001)
