
import random

from json_inout import ReadWriteJson as rwj
from mpyc.runtime import mpc
import csv
import base64
import pickle


async def main():
    """every party samples random values 'a' and 'b', but we only add the 'a' and 'b' of the first party and ignore the rest"""
    await mpc.start()

    name = "add.py_" + str(mpc.pid)


    inputstring = rwj.read_jsonfile(name)
    val = inputstring["data_str"]

    a = pickle.loads(base64.decodebytes(val.encode('utf-8')))

    aa = await mpc.output(a)

    print(f"{aa}")
    await mpc.shutdown()


mpc.run(main())