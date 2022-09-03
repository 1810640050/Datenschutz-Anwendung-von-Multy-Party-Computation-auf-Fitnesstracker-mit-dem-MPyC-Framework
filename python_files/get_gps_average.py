import json
import base64
import pickle
from mpyc.runtime import mpc
from math import sqrt
import math
import definitions as defs
from InOut import ReadWriteCSV as rwcsv
import sys
from time import time

secfxp = mpc.SecFxp()
secflt = mpc.SecFlt()
secint= mpc.SecInt()
file1=sys.stdout
file2=sys.stdout

async def main():
    await mpc.start()
    static_dx = mpc.input(secfxp(71.5))[0]
    static_dy = mpc.input(secfxp(111.3))[0]


    path = "../" + defs.PATH_FOR_GPS_SHARES
    name = path + "share_" + str(mpc.pid) + ".csv"

    sec_values = rwcsv.get_CSV_as_List(name)
    header_line = sec_values.pop(0)
    calc_list = []
    #counter = 1
    for line in sec_values:
        sec_lat = json.loads(line[0])
        sec_lon = json.loads(line[1])
        clear_date = json.loads(line[2])

        field_of_lat = pickle.loads(base64.decodebytes(sec_lat.encode('utf-8')))
        field_of_lon = pickle.loads(base64.decodebytes(sec_lon.encode('utf-8')))
        lat = secfxp(field_of_lat)
        lon = secfxp(field_of_lon)


        # read progress bar
        #string = "\rRead progress: " + str(round(counter/(len(sec_values))*100)) + "%"
        #file1.flush()
        #file1.write(string)
        #counter += 1

        calc_list.append([lat, lon])

    point1 = 0
    point2 = 1
    sec_distances = []
    start = time()
    for point in range(len(calc_list)-1):
        lat1 = calc_list[point1][0]
        lon1 = calc_list[point1][1]
        lat2 = calc_list[point2][0]
        lon2 = calc_list[point2][1]

        # "Die Konstante 111.3 ist dabei der Abstand zwischen zwei Breitenkreisen in km
        # und 71.5 der durchschnittliche Abstand zwischen zwei Längenkreisen in unseren Breiten."
        # https://www.kompf.de/gps/distcalc.html
        # dx = 71.5 * (lon1 - lon2)
        # dy = 111.3 * (lat1 - lat2)
        dx = static_dx * (lon1 - lon2)
        dy = static_dy * (lat1 - lat2)
        erg = mpc.pow(dx,2) + mpc.pow(dy, 2)
        #erg = dx * dx + dy * dy
        sec_distances.append(erg)

        # calculation progress bar
        #string = "\rCalculation Progress: " + str(round(point2 / (len(calc_list) - 1) * 100)) + "%"
        #file2.flush()
        #file2.write(string)

        # get next 2 Points:
        point1 += 1
        point2 += 1

    await mpc.gather(sec_distances)
    end = time()
    elapsed_time = end - start
    distances = await mpc.output(sec_distances)
    clear_distances = sum(map(sqrt, distances))

    printlist = ["Distance:",clear_distances, "m", "Critical time:", elapsed_time]
    #if mpc.pid == 0:

    print(printlist)
    rwcsv.WriteCSV("../" + defs.PATH_FOR_TEMP_FILES + defs.AVERAGE_FILE, 'a', printlist)
    await mpc.shutdown()
mpc.run(main())
