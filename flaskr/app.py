import os
from flask import Flask, render_template
from users.views import users

# APP CONFIGURATION
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='test'  # TODO: Configuration values here will later be put into a config.py
)
# BLUEPRINT REGISTRATION
app.register_blueprint(users)


# HOME PAGE
@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

