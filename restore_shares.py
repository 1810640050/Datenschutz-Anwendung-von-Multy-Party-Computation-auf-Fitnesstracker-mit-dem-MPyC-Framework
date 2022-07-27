
import random

from InOut import ReadWriteJson as rwj
from mpyc.runtime import mpc
import csv
import base64
import pickle


async def main():
    await mpc.start()

    # define name of file
    name = "share_" + str(mpc.pid) + ".json"

    # get computed string of shares
    inputstring = rwj.read_jsonfile(name)
    val = inputstring["data_str"]

    # restore to field
    a = pickle.loads(base64.decodebytes(val.encode('utf-8')))

    # compute shares
    aa = await mpc.output(a)

    print(f"Input Clear Value: {aa}")
    await mpc.shutdown()


mpc.run(main())