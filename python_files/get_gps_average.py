import json
import base64
import pickle
from mpyc.runtime import mpc
from math import sqrt
import definitions as defs
from InOut import ReadWriteCSV as rwcsv
import sys

secfxp = mpc.SecFxp()
file1=sys.stdout
file2=sys.stdout

async def main():
    await mpc.start()

    path = "../" + defs.PATH_FOR_GPS_SHARES
    name = path + "share_" + str(mpc.pid) + ".csv"

    sec_values = rwcsv.get_CSV_as_List(name)
    header_line = sec_values.pop(0)
    calc_list = []

    counter = 1
    for line in sec_values:
        sec_lat = json.loads(line[0])
        sec_lon = json.loads(line[1])
        clear_date = json.loads(line[2])

        field_of_lat = pickle.loads(base64.decodebytes(sec_lat.encode('utf-8')))
        field_of_lon = pickle.loads(base64.decodebytes(sec_lon.encode('utf-8')))

        lat = secfxp(field_of_lat)
        lon = secfxp(field_of_lon)
        string = "\rRead progress: " + str(counter) + "/" + str(len(sec_values))+ " "
        file1.flush()
        file1.write(string)
        counter += 1
        calc_list.append([lat, lon])


    point1 = 0
    point2 = 1
    distance = 0.0
    for point in range(len(calc_list)-1):
        lat1 = calc_list[point1][0]
        lon1 = calc_list[point1][1]
        lat2 = calc_list[point2][0]
        lon2 = calc_list[point2][1]

        # "Die Konstante 111.3 ist dabei der Abstand zwischen zwei Breitenkreisen in km
        # und 71.5 der durchschnittliche Abstand zwischen zwei Längenkreisen in unseren Breiten."
        # https://www.kompf.de/gps/distcalc.html
        dx = 71.5 * (lon1 - lon2)
        dy = 111.3 * (lat1 - lat2)
        base = mpc.pow(dx, 2) + mpc.pow(dy, 2)
        clear_base = await mpc.output(base)
        string = "\rCalculation Progress: " + str(point2) + "/" + str(len(calc_list)-1) + " " + str(distance) + "+" + str(sqrt(clear_base) * 1000) + "=" + str(distance + sqrt(clear_base) * 1000)
        file2.flush()
        file2.write(string)
        distance += sqrt(clear_base) * 1000 # *1000 -> meters

        # get next 2 Points:
        point1 += 1
        point2 +=1
    if mpc.pid == 0:
        rwcsv.WriteCSV("../" + defs.PATH_FOR_TEMP_FILES + defs.AVERAGE_FILE, 'a', ["Distance:",distance, "m"])
    await mpc.shutdown()
mpc.run(main())