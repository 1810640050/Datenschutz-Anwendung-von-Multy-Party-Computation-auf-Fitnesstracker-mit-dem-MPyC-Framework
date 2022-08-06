from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    items = []
    path = "./storage"
    files = os.listdir(path)
    for i in files:
        items.append(i)
    items.sort()
    return render_template("start.html", items=items)


@app.route("/admin")
def admin():
    return  render_template("admin.html")

@app.route("/versicherung")
def versicherung():
    return render_template("sichten.html")

@app.route("/show_data")
def show_data():
    #with open("./storage/") as file:
        #list = []
       # for line in file:
        #    list.append(line)
    return render_template("show_data.html")#, list=list)

