import json
import random
from datetime import date
from InOut import ReadWriteJson as rwj
from InOut import ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
from mpyc.runtime import mpc
import csv
import base64
import pickle


async def main():
    await mpc.start()

    # # define name of file
    # name = "share_" + str(mpc.pid) + ".json"
    #
    # # get computed string of shares
    # inputstring = rwj.read_Json_File(name)
    # val = inputstring["data_str"]
    #
    # # restore to field
    # a = pickle.loads(base64.decodebytes(val.encode('utf-8')))
    #
    # # compute shares
    # aa = await mpc.output(a)
    #
    # print(f"Input Clear Value: {aa}")



    # define name of filr
    name = "share_" + str(mpc.pid) + ".csv"
    clear_name = "daily_steps_decrypted.csv"

    # read csv file
    sec_values = rwcsv.get_CSV_as_List(name)
    header_line = sec_values.pop(0)
    rwcsv.WriteCSV(clear_name, 'w', header_line)
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
        clear_values = [id, clear_date, clear_value_of_steps]

        # only node 0 writes to file
        if mpc.pid == 0:
            rwcsv.WriteCSV(clear_name, 'a', clear_values)

    await mpc.shutdown()
mpc.run(main())