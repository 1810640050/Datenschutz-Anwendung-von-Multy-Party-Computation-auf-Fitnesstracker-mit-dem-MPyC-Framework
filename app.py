from flask import Flask, render_template, request
import os

app = Flask(__name__)

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