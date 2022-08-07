import csv
import json

from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os

import definitions

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
    return render_template("admin.html")


@app.route("/versicherung")
def versicherung():
    list = []
    with open('./storage/Averages.csv', 'r') as file:
        data = csv.reader(file, delimiter=',')
        for line in data:
            list.append(line)
    head = list[0]

    # listenelemente sind strings und keine listen!!
    all_months = get_list_of_stringlist(list[1])
    all_years = get_list_of_stringlist(list[2])
    all_steps_ever = get_list_of_stringlist(list[3])

    year = request.args.get("year", "choose year")
    month = request.args.get("month", "choose month")

    all_months_filter = []

    for i in all_months:
        if str(i[0]).startswith(str(year)+"-"+str(month)):
            all_months_filter.append(i)


    return render_template("sichten.html", all_months_filter=all_months_filter, month=month, year=year, title="page", years=definitions.YEARS, months=definitions.MONTHS ,head=head, all_months=all_months,
                           all_years=all_years, all_steps_ever=all_steps_ever, list=list)

# string in liste umwandeln
def get_list_of_stringlist(list):
    import ast
    returnlist = []
    for i in list:
        returnlist.append(ast.literal_eval(i))
    return returnlist
