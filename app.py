from python_files.InOut import ReadWriteCSV as rwcsv
import python_files.definitions as defs
from flask import Flask, request, render_template
import os

app = Flask(__name__)

FILTERED_LIST = []
@app.route("/")
def hello_world():
    items = []
    path = defs.PATH_FOR_SHARES
    files = os.listdir(path)
    if len(files) == defs.PARTIES:
        complete = "All files complete! " + str(defs.PARTIES) + " Parties defined and " + str(len(files)) + " Shares available"
    else:
        complete = "ERROR, some files are missing! " + str(len(files)) + " Shares and " + str(defs.PARTIES) + " Parties were defined!"
    for i in files:
        items.append([i, path])
    items.sort()
    return render_template("start.html", items=items, complete=complete)


@app.route("/admin")
def admin():
    function = request.args.get("Choose_Function", defs.FUNCTIONS[0])
    returnlist = []
    if function == defs.FUNCTIONS[1]:
        returnlist = [defs.FUNCTIONS[1]]
    elif function == defs.FUNCTIONS[2]:
        returnlist = [defs.FUNCTIONS[2]]
    elif function == defs.FUNCTIONS[3]:
        returnlist = [defs.FUNCTIONS[3]]

    return render_template("admin.html",function=function, functions=defs.FUNCTIONS, returnlist=returnlist)


@app.route("/versicherung")
def versicherung():
    average_file = defs.AVERAGE_FILE
    year = request.args.get("year", "---")
    month = request.args.get("month", "---")
    searchstring = " " + str(year) + " " + str(month)
    os.system(defs.RUN_AVERAGE_SCRIPT + searchstring)
    list = rwcsv.get_CSV_as_List(defs.PATH_FOR_TEMP_FILES + average_file)
    file_path = defs.PATH_FOR_TEMP_FILES + average_file
    if os.path.isfile(file_path):
        os.remove(file_path)
    return render_template("sichten.html",special_month=defs.MONTHS_SPECIALS, special_year=defs.YEARS_SPECIALS, zeitraum=defs.ZEITRAUM, schritte=defs.SCHRITTE, month=month, year=year, years=defs.YEARS, months=defs.MONTHS, list=list)


# # string in liste umwandeln
def get_list_of_stringlist(list):
    import ast
    returnlist = []
    for i in list:
        returnlist.append(ast.literal_eval(i))
    return returnlist

if __name__ == '__main__':
    app.run(debug=True)
