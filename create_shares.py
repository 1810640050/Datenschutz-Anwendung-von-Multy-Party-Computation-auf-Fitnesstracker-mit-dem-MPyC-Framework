import random
from mpyc.runtime import mpc
import csv
import base64
import pickle
import json
from json_inout import ReadWriteJson as rwj


secint = mpc.SecInt()

async def main():
    await mpc.start()
    name = "share_" + str(mpc.pid) + ".json"
    random_input = rwj.read_jsonfile("ran_val")["ranval"]

    n = mpc.input(secint(random_input))[0]


    gather_n = await mpc.gather(n)
    str_of_gather = str(gather_n)

    print("value",gather_n.value)


    str_decode_n = base64.encodebytes(pickle.dumps(gather_n)).decode()
    print("sid_data_str ", str_decode_n)
    sid_data_restore = pickle.loads(base64.decodebytes(str_decode_n.encode('utf-8')))

    dict_n = {
        "random input": random_input,
        "int": str_of_gather,
        "string": str(str_decode_n),
        "restore": str(sid_data_restore)
    }

    print(dict_n)

    rwj.create_jsonfile(name, 'w', dict_n)

    list_values = rwj.read_jsonfile(name)

    print("random input ", type(list_values["random input"]), list_values["random input"])
    print("int ", type(list_values["int"]), list_values["int"])
    print("string ", type(list_values["string"]), list_values["string"])
    print("restore ", type(list_values["restore"]), list_values["restore"])


    await mpc.shutdown()
mpc.run(main())