MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
YEARS = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]
YEARS_SPECIALS = ["All_Data_all_time"]
MONTHS_SPECIALS = ["All_Months_of_chosen_year", "All_Data_of_chosen_year"]
NODATA = "No Data available!"
HEADER = ["Id", "Zeitraum", "Schritte"]
PARTIES = 3
PATH_FOR_SHARES = "storage/"
PATH_FOR_INPUTFILES = "inputfiles/"
PATH_FOR_TEMP_FILES = "tmp/"
PATH_FOR_PYTHON_FILES = "python_files/"
ZEITRAUM = "Zeitraum"
SCHRITTE = "Schritte"
AVERAGE_FILE = "average.csv"
FUNCTIONS = ["---", "Create_Inputvalues", "Delete_Inputvalues", "Create_Shares", "Delete_Shares"]
RUN_AVERAGE_SCRIPT = "python " + PATH_FOR_PYTHON_FILES + "get_average.py -M" + str(PARTIES)
RUN_CREATE_INPUTVALUES = "python " + PATH_FOR_PYTHON_FILES + "create_inputvalues.py"
RUN_CREATE_SHARES = "python " + PATH_FOR_PYTHON_FILES + "create_shares.py -M" + str(PARTIES)
UPLOAD_FOLDER = "inputfiles/"
ALLOWED_EXTENSIONS = {'csv'}
WEBHOOK_PATHS = ["https://webhook.site/ef5d85a8-69b3-4a5c-a027-85446c1a622c", "https://webhook.site/e3f3baef-40f2-4a0f-b32d-5542bd504c51", "https://webhook.site/2a7a69de-7670-458d-bff3-8e5b6b13abfb"]




