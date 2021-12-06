from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from users.views import users
import mysql.connector as mysql
from sshtunnel import SSHTunnelForwarder

import pymysql

# APP CONFIGURATION
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='test',  # TODO: Configuration values here will later be put into a config.py
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://csc2033_team08:HumsBury7Pop@cs-db.ncl.ac.uk:3306/csc2033_team08',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
sql_hostname = 'cs-db.ncl.ac.uk'
sql_username = 'csc2033_team08'
sql_password = 'HumsBury7Pop'
sql_main_database = 'csc2033_team08'
sql_port = 3306
ssh_host = 'linux.cs.ncl.ac.uk'
ssh_user = 'c0046720'
ssh_port = 22
sql_ip = '127.0.0.1'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password="your_uni_password_here",
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    print(conn)
    conn.close()
db = SQLAlchemy(app)
print(db)

# blueprint registration
app.register_blueprint(users)


@app.route('/')
def index():
    return render_template("index.html")


# error pages
@app.errorhandler(400)
def page_forbidden(_error):
    return render_template('errors/400.html'), 400


@app.errorhandler(403)
def page_not_found(_error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def internal_error(_error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(_error):
    return render_template('errors/500.html'), 500


@app.errorhandler(503)
def internal_error(_error):
    return render_template('errors/503.html'), 503


if __name__ == '__main__':
    app.run(debug=True)


