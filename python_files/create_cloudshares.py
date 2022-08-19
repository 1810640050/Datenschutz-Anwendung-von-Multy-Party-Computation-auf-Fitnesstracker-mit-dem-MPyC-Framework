from InOut import ReadWriteJson as rwj, ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
import base64
import pickle
import json
from mpyc.runtime import mpc
import definitions as defs
import sys
import requests

async def main():
    await mpc.start()

    name = "../" + defs.PATH_FOR_SHARES + "share_" + str(mpc.pid) + ".csv"
    cloudpath = defs.WEBHOOK_PATHS[0]
    print("Cloudpath: ", cloudpath)
    # read csv file and store clear values in list
    #sec_values = rwcsv.get_CSV_as_List(name)

    with open(name, 'r') as f:
        r = requests.post(cloudpath, f)
    print("r ", r.text)
    #token = r.headers["X-Token-Id"]
    #ID = r.headers["X-Request-Id"]

    #print(token, " ", ID)

    #get_link = "https://webhook.site/token/" + token + "/request/" + ID + "/raw"

    # rwcsv.WriteCSV(defs.PATH_FOR_SHARES + "GETLINKS", 'w')
    # link_dict = {mpc.pid: get_link}
    # rwcsv.WriteCSV(defs.PATH_FOR_SHARES + "GETLINKS", 'a', link_dict)
    await mpc.shutdown()
mpc.run(main())

