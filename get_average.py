from InOut import ReadWriteCSV as rwcsv
from InOut import ComputeDates as comDt
import base64
import pickle
import json
from mpyc.runtime import mpc


async def main():
    await mpc.start()

    # define name of file
    name = "share_" + str(mpc.pid) + ".csv"
    clear_name = "daily_steps_decrypted.csv"

    # read csv file and store clear values in list
    sec_values = rwcsv.get_CSV_as_List(name)
    header_line = sec_values.pop(0)
    clear_values = []
    for line in sec_values:
        id = int(line[0])
        sec_date = json.loads(line[1])
        sec_steps = json.loads(line[2])

        # restore to field
        field_of_date = pickle.loads(base64.decodebytes(sec_date.encode('utf-8')))
        field_of_steps = pickle.loads(base64.decodebytes(sec_steps.encode('utf-8')))

        # compute values
        clear_value_of_timestamp = await mpc.output(field_of_date)
        clear_value_of_steps = await mpc.output(field_of_steps)

        # get date from timestamp
        clear_date = comDt.get_Datetime_of_Timestamp(clear_value_of_timestamp).date()

        clear_values.append([id, clear_date, int(clear_value_of_steps)])
    await mpc.shutdown()

    try:
        print("1. Durchschnitt ein Monat\n2. Durchschnitt ein Jahr\n3. Durchschnitt aller Monate eines Jahres\n4. Durchschnitt gesamt\n5. Beenden")
        choice = input("Ihre Eingabe:")

        if choice == 1 or choice == '1':
            print("Menü 1: Durchschnitt eines Monats gewählt.")
            steps = 0
            counter = 0
            jahr = input("Jahr wählen (4-stellig): ")
            monat = input("Monat wählen (2-stellig): ")
            searchstring = str(jahr) + "-" + str(monat)
            for i in clear_values:
                datum = str(i[1])
                if datum.startswith(searchstring):
                    steps += i[2]
                    counter += 1
            print("Steps: ", steps, " Counter: ", counter)
            print("Monatsschnitt von " + searchstring + ": ", round(steps / counter))

        elif choice == 2 or choice == '2':
            print("Menü 2: Durchschnitt eines Jahres gewählt.")
            jahr = input("Jahr eingeben")
            steps = 0
            counter = 0
            jahr = input("Jahr wählen (4-stellig): ")
            searchstring = str(jahr)
            for i in clear_values:
                datum = str(i[1])
                if datum.startswith(searchstring):
                    steps += i[2]
                    counter += 1
            print("Steps: ", steps, " Counter: ", counter)
            print("Jahre3sschnitt von " + searchstring + ": ", round(steps / counter))

        elif choice == 3 or choice == '3':
            print("Menü 3: Durchschnitt aller Monate eines Jahres gewählt.")
            jahr = input("Jahr wählen (4-stellig): ")
            all_months = []
            for i in range(1,13):
                steps = 0
                counter = 0
                searchstring = str(jahr) + "-" + "{:02d}".format(i)
                for i in clear_values:
                    datum = str(i[1])
                    if datum.startswith(searchstring):
                        steps += i[2]
                        counter += 1
                erg = round(steps/counter)
                erg_string = str(searchstring) + ": " + str(erg)
                all_months.append(erg_string)
            for i in all_months:
                print(i)

        elif choice == 4 or choice == '4':
            print("Menü 4: Durchschnitt gesamt gewählt")
            steps = 0
            divisor = len(clear_values)
            for i in clear_values:
                steps += i[2]
            print("Average steps all Time: ", round(steps / divisor))
        elif choice == 5 or choice == '5':
            a = 0
        else:
            print("Eingabefehler -- ELSE --")
    except:
        print("Eingabefehler -- Exception --")


mpc.run(main())