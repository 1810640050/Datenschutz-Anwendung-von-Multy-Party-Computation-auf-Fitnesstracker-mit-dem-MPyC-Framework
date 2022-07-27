import random

from InOut import ReadWriteJson as rwj
from mpyc.runtime import mpc
import csv
import base64
import pickle


secint = mpc.SecInt()


async def main():
    await mpc.start()
    # define name for files with shares -> share_x.json
    name = "share_" + str(mpc.pid) + ".json"

    # get input from json file
    ran = rwj.read_jsonfile("input_values.json")
    ran = ran["value"]

    #if type(ran) == str:


    # take input and start mpc computing
    a = mpc.input(secint(ran))[0]  # array von inputs von jedem knoten, immer den ersten wert [0] - node 0

    # get Field of secint
    sid_data_gf = await mpc.gather(a)
    # convert to string
    sid_data_str = base64.encodebytes(pickle.dumps(sid_data_gf)).decode()

    # store string in dictionary and save to json
    dict = {
        "data_str": sid_data_str,
    }
    rwj.create_jsonfile(name,'w', dict)


    await mpc.shutdown()
mpc.run(main())