import base64
import json
import pickle

from InOut import ReadWriteCSV as rwcsv
from mpyc.runtime import mpc

secint = mpc.SecInt()


async def main():
    await mpc.start()

    # # define name for files with shares -> share_x.json
    # name = "share_" + str(mpc.pid) + ".json"

    # # get input from json file
    # ran = rwj.read_Json_File("input_values.json")
    # ran = ran["value"]
    # # take input and start mpc computing
    # a = mpc.input(secint(ran))[0]  # array von inputs von jedem knoten, immer den ersten wert [0] - node 0
    #
    # # get Field of secint
    # sid_data_gf = await mpc.gather(a)
    # # convert to string
    # sid_data_str = base64.encodebytes(pickle.dumps(sid_data_gf)).decode()
    #
    # # store string in dictionary and save to json
    # dict = {
    #     "data_str": sid_data_str,
    # }
    # rwj.create_Json_File(name, 'w', dict)


    # define name for files with shares -> share_x.csv
    name = "share_" + str(mpc.pid) + ".csv"

    # get input from csv file
    csv_values = rwcsv.get_CSV_as_List("daily_steps.csv")
    header_line = csv_values.pop(0)
    rwcsv.WriteCSV(name, 'w', header_line)
    sec_values = []
    for line in csv_values:
        id = line[0]
        date = int(line[1])
        steps = int(line[2])

        # take input and start mpc computing
        sec_date = mpc.input(secint(date))[0]
        sec_steps = mpc.input(secint(steps))[0]

        # get field of secint
        field_of_date = await mpc.gather(sec_date)
        field_of_steps = await mpc.gather(sec_steps)

        # convert to string
        string_of_datefield = base64.encodebytes(pickle.dumps(field_of_date)).decode()
        string_of_stepsfield = base64.encodebytes(pickle.dumps(field_of_steps)).decode()

        # store values to list and store to csv
        json_id = json.dumps(id)
        json_date = json.dumps(string_of_datefield)
        json_steps = json.dumps(string_of_stepsfield)
        valuelist = [id, json_date, json_steps]
        rwcsv.WriteCSV(name, 'a', valuelist)

    await mpc.shutdown()
mpc.run(main())