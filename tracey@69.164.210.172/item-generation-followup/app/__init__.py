from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

app = Flask(__name__)
#with open('/etc/config.json') as config_file:
#    config = json.load(config_file)
app.config['SECRET_KEY'] = 'xx'#config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///local_test.db"  #config.get('SQLALCHEMY_DATABASE_URI') #make local db for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
from . import views
if __name__ == '__main__':
    app.run()



#export FLASK_APP=__init__.py
#flask shell
#from robot_app import db
#db.create_all()

#flask run 

#sqlite3
#.open local3.db
#select * from trials;
#https://inloop.github.io/sqlite-viewer/

#ssh tracey@69.164.210.172
#screen -ls
#screen -d to detach
#screen -r to reattach

#to run locally, url in views and experiment should be "/"
#to run on server, url = '/botstudy' and 'botstudy'
#li125-172.members.linode.com

#screen
#gunicorn -w 9 <dir to folder containing init file>: app
#ctr a then d

#might need to do ps-A then kill gunicorn tasks if not working

#sqlite-utils server_db.db "select * from trials" --json-cols > trials.json to get data