import random

from json_inout import ReadWriteJson as rwj
from mpyc.runtime import mpc
import csv
import base64
import pickle


secint = mpc.SecInt()


async def main():
    """every party samples random values 'a' and 'b', but we only add the 'a' and 'b' of the first party and ignore the rest"""
    await mpc.start()

    name = "add.py_" + str(mpc.pid)

    # für a aus file lesen dann brauche ich kein mpc.input
    # input im "fitnesstracker" am server
    # 3 Knoten verwenden
    # TODO Secint dump vom binary
    ran = rwj.read_jsonfile("ran_val")
    print("random: ", ran)
    ran = ran["ranval"]

    a = mpc.input(secint(ran))[0]  # array von inputs von jedem knoten, immer den ersten wert [0] - node 0

    # sid_data ist ein secint

    sid_data_gf = await mpc.gather(a)
    print("sid_data_gf ", sid_data_gf)
    sid_data_str = base64.encodebytes(pickle.dumps(sid_data_gf)).decode()
    print("sid_data_str ", sid_data_str, " type: ", type(sid_data_str))
    sid_data_restore = pickle.loads(base64.decodebytes(sid_data_str.encode('utf-8')))
    print("sid_data_restore ", sid_data_restore)

    datastring = [i for i in sid_data_str]
    #datarestore = [i for i in sid_data_restore]
    #datagf = [i for i in sid_data_gf]

    #print(datastring, datagf, datagf)

    dict = {
        "data_str": sid_data_str,
        "data_gf": str(sid_data_gf),
        "data_restore": str(sid_data_restore),
        "clear value": ran
    }

    rwj.create_jsonfile(name,'w', dict)

    # inputstring = rwj.read_jsonfile(name)
    # val = inputstring["data_str"]
    #
    # a = pickle.loads(base64.decodebytes(val.encode('utf-8')))
    #
    # aa = await mpc.output(a)
    #
    # print(f"{aa}")
    await mpc.shutdown()


mpc.run(main())