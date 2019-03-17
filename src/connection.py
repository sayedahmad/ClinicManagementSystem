from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from eralchemy import render_er

app=Flask(__name__, template_folder='../templates', static_folder='../static')


app.config['SQLALCHEMY_DATABASE_URI']='mysql://clinic:clinic123@localhost:3306/cms'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

app.config['WHOOSH_BASE']='whoosh'
app.config['DEBUG']=True
app.config['SECRET_KEY']='thisismysecretkeywhichneverexpires'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_FORGOT_PASSWORD'] = False
app.config['USER_ENABLE_REGISTER'] = False
app.config['USER_AFTER_LOGIN_ENDPOINT'] = 'redirection'

app.config[''] = False
db=SQLAlchemy(app)

# render_er('mysql://clinic:clinic123@localhost:3306/cms', 'erd_from_sqlalchemy.png')
