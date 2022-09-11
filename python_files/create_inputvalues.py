from mpyc.runtime import mpc
from InOut import ReadWriteJson as rwj
from InOut import ReadWriteCSV as rwcsv
from datetime import date, time, datetime
import csv, json
import definitions as defs


def _get_Timestamp_of_String(timestring):
    d = datetime.strptime(timestring, "%Y:%m:%d")
    return int(round(datetime.timestamp(d)))

def _get_Datetime_of_Timestamp(stamp):
    return datetime.fromtimestamp(stamp)

def run():
    name = defs.PATH_FOR_INPUTFILES + "dailySteps_merged.csv"
    daily_steps = rwcsv.get_CSV_as_List(name)
    daily_steps_csv = daily_steps

    # create csv file
    #name = "daily_steps.csv"
    daily_steps_csv.pop(0)
    header_line = defs.HEADER

    rwcsv.WriteCSV(name, 'w', header_line)

    for i in daily_steps_csv:
        id = i[0]
        date = _get_Timestamp_of_String(i[1])
        steps = int(i[2])
        list = [id, date, steps]
        rwcsv.WriteCSV(name, 'a', list)

run()





