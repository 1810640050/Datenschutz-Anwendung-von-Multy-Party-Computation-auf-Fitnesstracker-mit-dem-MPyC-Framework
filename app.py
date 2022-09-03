import requests

from python_files.InOut import ReadWriteCSV as rwcsv
import python_files.definitions as defs
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = defs.UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in defs.ALLOWED_EXTENSIONS

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    items = []
    path = defs.PATH_FOR_INPUTFILES
    files = os.listdir(path)
    for i in files:
        items.append([i, path])
    items.sort()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('admin', name=filename))


    # FUNCTIONS = ["---", "Create_Inputvalues_with_Date", "Delete_Inputvalues", "Create_Shares_with_Date", "Delete_Shares"]
    function = request.args.get("Choose_Function", defs.FUNCTIONS[0])
    returnlist = []
    if function == defs.FUNCTIONS[1]:
        path = defs.PATH_FOR_INPUTFILES
        input_files = os.listdir(path)
        if len(input_files) != 1:
            return render_template("error.html", error="1 File required!")
        elif len(input_files) == 1 and os.path.isfile(path + str(input_files[0])):
            print("Skript wird ausgeführt")
            os.system(defs.RUN_CREATE_INPUTVALUES)
        returnlist = ["1." + defs.FUNCTIONS[1]]
    elif function == defs.FUNCTIONS[2]:
        path = defs.PATH_FOR_INPUTFILES
        files = os.listdir(path)
        for file in files:
            file_path = path + str(file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        returnlist = ["2." + defs.FUNCTIONS[2]]
        return redirect(url_for('admin'))
    elif function == defs.FUNCTIONS[3]:
        os.system(defs.RUN_CREATE_SHARES)
        returnlist = ["3." + defs.FUNCTIONS[3]]
    elif function == defs.FUNCTIONS[4]:
        path = defs.PATH_FOR_SHARES
        files = os.listdir(path)
        for file in files:
            file_path = path + str(file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        returnlist = ["4." + defs.FUNCTIONS[4]]
        return redirect(url_for('admin'))


    return render_template("admin.html",items=items, function=function, functions=defs.FUNCTIONS, returnlist=returnlist)


@app.route("/versicherung", methods=['GET'])
def versicherung():
    # aufpandas ändern!!!
    average_file = defs.AVERAGE_FILE
    year = request.args.get("year", "---")
    month = request.args.get("month", "---")
    searchstring = " " + str(year) + " " + str(month)[:2]

    if len(request.args) == 0: # Seite wird ohne Parameter aufgerufen
        return render_template("sichten.html",special_month=defs.MONTHS_SPECIALS, special_year=defs.YEARS_SPECIALS, zeitraum=defs.ZEITRAUM, schritte=defs.SCHRITTE, month=month, year=year, years=defs.YEARS, months=defs.MONTHS)

    elif len(request.args) > 0: # nur mit Suchparameter wird mpc gestartet
        print("Searchstring: ", searchstring)
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
