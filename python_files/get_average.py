from InOut import ReadWriteJson as rwj, ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
import base64
import pickle
import json
from mpyc.runtime import mpc
import definitions as defs
import sys


args = sys.argv

async def main():
    if len(args) != 3:
        return ["ERROR", "Invalid number of arguments!"]
    else:
        own_name = args.pop(0)
        year = args[0]
        month = args[1]

        await mpc.start()

        # define searchstring
        searchstring = str(year) + "-" + str(month)

        # define name of file
        name = defs.PATH_FOR_SHARES + "share_" + str(mpc.pid) + ".csv"

        # read csv file and store clear values in list
        sec_values = rwcsv.get_CSV_as_List(name)
        header_line = sec_values.pop(0)
        clear_values = []
        for line in sec_values:
            id = int(line[0])
            sec_date = json.loads(line[1])
            sec_steps = json.loads(line[2])

            # restore to field
            field_of_date = pickle.loads(base64.decodebytes(sec_date.encode('utf-8')))
            field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))

            # compute values
            clear_value_of_timestamp = await mpc.output(field_of_date)
            clear_value_of_steps = await mpc.output(field_of_steps)

            # get date from timestamp
            clear_date = comDt.get_Datetime_of_Timestamp(clear_value_of_timestamp).date()

            # if date fits searchstring -> store in list
            if str(clear_date).startswith(searchstring):
                clear_values.append([id, str(clear_date), int(clear_value_of_steps)])

        summe = 0
        for i in clear_values:
            summe += i[2]
        divisor = len(clear_values)
        if divisor < 1:
            average_steps = "No Data"
        else:
            average_steps = round(summe/divisor)
        if mpc.pid == 0:
            rwcsv.WriteCSV(defs.PATH_FOR_TEMP_FILES + "average.csv", 'w', [id, searchstring, average_steps])
        await mpc.shutdown()



mpc.run(main())

