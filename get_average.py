from InOut import ReadWriteJson as rwj, ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
import base64
import pickle
import json
from mpyc.runtime import mpc
import definitions as defs


async def main():
    await mpc.start()

    # define name of file
    name = "share_" + str(mpc.pid) + ".csv"
    clear_name = "daily_steps_decrypted.csv"

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

        clear_values.append([id, clear_date, int(clear_value_of_steps)])
    print("\nDurchschnitt aller Monate aller Jahre:")
    filename = "Averages.csv"
    ueberschrift = ["Durchschnitt aller Monate aller Jahre", "Steps"]
    if mpc.pid == 0:
        rwcsv.WriteCSV(filename, 'w', ueberschrift)
    months = defs.MONTHS
    years = defs.YEARS

    for i in years:
        for j in months:
            steps = 0
            counter = 0
            searchstring = i + "-" + j
            for k in clear_values:
                datum = str(k[1])
                if datum.startswith(searchstring):
                    steps += k[2]
                    counter += 1
            if counter < 1:
                print(searchstring, ": No Data awailable")
                if mpc.pid == 0:
                    rwcsv.WriteCSV(filename, 'a',[searchstring, "No Data awailable"])
            else:
                print(searchstring, ": ", round(steps / counter))
                if mpc.pid == 0:
                    rwcsv.WriteCSV(filename, 'a', [searchstring, round(steps / counter)])
            steps = 0
            counter = 0

    print("\nDurchschnitt aller Jahre:")
    ueberschrift2 = ["Durchschnitt aller Jahre", "Steps"]
    if mpc.pid == 0:
        rwcsv.WriteCSV(filename, 'a', ueberschrift2)
    years = defs.YEARS
    for year in years:
        steps = 0
        counter = 0
        searchstring = year
        for i in clear_values:
            datum = str(i[1])
            if datum.startswith(searchstring):
                steps += i[2]
                counter += 1
        if counter < 1:
            print(searchstring, ": No Data awailable")
            if mpc.pid == 0:
                rwcsv.WriteCSV(filename, 'a', [searchstring, "No Data awailable"])
        else:
            print(searchstring, ": ", round(steps / counter))
            if mpc.pid == 0:
                rwcsv.WriteCSV(filename, 'a', [searchstring, round(steps / counter)])

    print("\nDurchschnitt gesamt:")
    ueberschrift3 = ["Durchschnitt gesamt", "Steps"]
    if mpc.pid == 0:
        rwcsv.WriteCSV(filename, 'a', ueberschrift3)
    steps = 0
    divisor = len(clear_values)
    for i in clear_values:
        steps += i[2]
    if divisor < 1:
        print(searchstring, ": No Data awailable")
        if mpc.pid == 0:
            rwcsv.WriteCSV(filename, 'a', [searchstring, "No Data awailable"])
    else:
        print(searchstring, ": ", round(steps / divisor))
        if mpc.pid == 0:
            rwcsv.WriteCSV(filename, 'a', ["Gesamt", round(steps / divisor)])
    print("Average steps all Time: ", round(steps / divisor))

    await mpc.shutdown()
mpc.run(main())

