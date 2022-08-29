from InOut import ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
import base64
import pickle
import json
from mpyc.runtime import mpc
import definitions as defs
import sys


args = sys.argv
secint = mpc.SecInt()

async def main():
    await mpc.start()
    if len(args) != 3:
        return ["ERROR", "Invalid number of arguments!"]
    else:


        own_name = args.pop(0) # => scriptname
        year = args[0]
        month = args[1]
        searchstring = None

        # define name of file
        name = defs.PATH_FOR_SHARES + "share_" + str(mpc.pid) + ".csv"

        # read csv file and store clear values in list
        sec_values = rwcsv.get_CSV_as_List(name)
        header_line = sec_values.pop(0)
        clear_values = []
        resultlist = []



        if str(month) == defs.MONTHS_SPECIALS[0]: # All Month each of chosen Year
            if mpc.pid == 0:
                rwcsv.WriteCSV(defs.PATH_FOR_TEMP_FILES + defs.AVERAGE_FILE, 'w')
            for month in defs.MONTHS:
                searchstring = str(year) + "-" + str(month)

                for line in sec_values:
                    id = int(line[0])
                    sec_date = json.loads(line[1])
                    #sec_steps = json.loads(line[2])

                    # restore to field
                    field_of_date = pickle.loads(base64.decodebytes(sec_date.encode('utf-8')))
                    #field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))

                    # compute values
                    clear_value_of_timestamp = await mpc.output(field_of_date)
                    #clear_value_of_steps = await mpc.output(field_of_steps)

                    # get date from timestamp
                    clear_date = comDt.get_Datetime_of_Timestamp(clear_value_of_timestamp).date()

                    # if date fits searchstring -> store in list
                    if str(clear_date).startswith(searchstring):
                        sec_steps = json.loads(line[2])
                        field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))
                        clear_values.append([id, str(clear_date), secint(field_of_steps)])

                appendlist = []
                summe = secint(0)
                for i in clear_values:
                    summe += i[2]
                divisor = len(clear_values)
                if divisor < 1:
                    average_steps = "No Data"
                    appendlist = [id, searchstring, average_steps]
                else:
                    erg = await mpc.output(summe)
                    average_steps = round(erg / divisor)
                    appendlist = [id, searchstring, average_steps]
                if mpc.pid == 0:
                    rwcsv.WriteCSV(defs.PATH_FOR_TEMP_FILES + defs.AVERAGE_FILE, 'a', appendlist)

        else:
            if str(year) == defs.YEARS_SPECIALS[0]: # all data all time
                searchstring = ""
            elif str(month) == defs.MONTHS_SPECIALS[1]: # All Data of chosen year
                searchstring = str(year)
            else: # regular requests => year and month
                searchstring = str(year) + "-" + str(month)

            for line in sec_values:
                id = int(line[0])
                sec_date = json.loads(line[1])
                #sec_steps = json.loads(line[2])

                # restore to field
                field_of_date = pickle.loads(base64.decodebytes(sec_date.encode('utf-8')))
                #field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))

                # compute values
                clear_value_of_timestamp = await mpc.output(field_of_date)
                #clear_value_of_steps = await mpc.output(field_of_steps)

                # get date from timestamp
                clear_date = comDt.get_Datetime_of_Timestamp(clear_value_of_timestamp).date()

                # if date fits searchstring -> store in list
                if str(clear_date).startswith(searchstring):
                    sec_steps = json.loads(line[2])
                    field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))
                    clear_values.append([id, str(clear_date), secint(field_of_steps)])

            summe = secint(0)
            for i in clear_values:
                summe += i[2]
            divisor = len(clear_values)
            if divisor < 1:
                average_steps = "No Data"
                resultlist = [id, searchstring, average_steps]
            else:
                if str(year) == defs.YEARS_SPECIALS[0]: # all data all time
                    searchstring = "all Data all Time"
                erg = await mpc.output(summe)
                average_steps = round(erg/divisor)
                resultlist = [id, searchstring, average_steps]
                #print("Resultlist: ", resultlist)
            if mpc.pid == 0:
                rwcsv.WriteCSV(defs.PATH_FOR_TEMP_FILES + defs.AVERAGE_FILE, 'w', resultlist)
    await mpc.shutdown()

mpc.run(main())

