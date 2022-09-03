from datetime import date, time, datetime
from mpyc.runtime import mpc
from InOut import ReadWriteCSV as rwcsv
import definitions as defs
import base64
import json
import pickle
from dateutil.parser import parse

secfxp = mpc.SecFxp()
secflt = mpc.SecFlt()



async def main():
    await mpc.start()

    list = rwcsv.get_CSV_as_List("../"+defs.PATH_FOR_GPS_INPUTFILES + defs.NAME_OF_GPS_INPUTFILE)
    list.pop(0)
    header_line = ["latitide", "longitude", "date"]
    path = "../" + defs.PATH_FOR_GPS_SHARES
    name = path + "share_" + str(mpc.pid) + ".csv"
    rwcsv.WriteCSV(name, 'w', header_line)

    for i in range(len(list ) -1):
        latitude = float(list[i][1])
        longitude = float(list[i][0])
        date = parse(list[i][6], ignoretz=True)
        stamp = round(datetime.timestamp(date))

        sec_lat = mpc.input(secfxp(latitude))[0]
        sec_lon = mpc.input(secfxp(longitude))[0]

        field_of_lat = await mpc.gather(sec_lat)
        field_of_lon = await mpc.gather(sec_lon)

        string_of_latfield = base64.encodebytes(pickle.dumps(field_of_lat)).decode()
        string_of_lonfield = base64.encodebytes(pickle.dumps(field_of_lon)).decode()

        json_lat = json.dumps(string_of_latfield)
        json_lon = json.dumps(string_of_lonfield)

        valuelist = [json_lat, json_lon, stamp]
        rwcsv.WriteCSV(name, 'a', valuelist)

    await mpc.shutdown()

mpc.run(main())