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
            auswahl = ShowMenu("Create Random", "Create and distribute Shares", "Compute Shares")

            if(auswahl == 1) or (auswahl == '1'):
                exec(open("create_inputvalues.py").read())
            elif(auswahl == 2) or (auswahl == '2'):
                exec(open("create_shares.py").read())
            elif(auswahl == 3) or (auswahl == '3'):
                exec(open("restore_shares.py").read())
            else:
                print("Programm finished!")
                a = 2
        except KeyboardInterrupt:
            print('\nExitting...')
            sys.exit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
