import sys
from InOut import ReadWriteJson as rwj


def ShowMenu(*args):
    print("")
    counter = 1
    for i in args:
        print(counter, "."+i)
        counter += 1

    auswahl = input("Nummer eingeben:")
    return auswahl




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = 1
    while a == 1:
        try:
            auswahl = ShowMenu("Create Random", "Create and distribute Shares", "Show Shares", "Compute Shares")

            if(auswahl == 1) or (auswahl == '1'):
                exec(open("create_random.py").read())
            elif(auswahl == 2) or (auswahl == '2'):
                exec(open("create_shares.py").read())
            elif (auswahl == 3) or (auswahl == '3'):
                stringlist = []
                stringlist.append(rwj.read_jsonfile("share_0.json"))
                stringlist.append(rwj.read_jsonfile("share_1.json"))
                stringlist.append(rwj.read_jsonfile("share_2.json"))
                counter = 1
                for i in stringlist:
                    print("File " + str(counter), i)
                    counter += 1
                counter = 1
            elif(auswahl == 4) or (auswahl == '4'):
                exec(open("restore_shares.py").read())


            else:
                print("Programm finished!")
                a = 2
        except KeyboardInterrupt:
            print('\nExitting...')
            sys.exit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
