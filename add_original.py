import random
from mpyc.runtime import mpc
import csv
import base64
import pickle

secint = mpc.SecInt()


async def main():
    """every party samples random values 'a' and 'b', but we only add the 'a' and 'b' of the first party and ignore the rest"""
    await mpc.start()

    # für a aus file lesen dann brauche ich kein mpc.input
    # input im "fitnesstracker" am server
    # 3 Knoten verwenden
    # TODO Secint dump vom binary
    ran = random.randint(0,10)
    print("random: ", ran)
    a = mpc.input(secint(ran))[0]  # array von inputs von jedem knoten, immer den ersten wert [0] - node 0
    b = mpc.input(secint(random.randint(0, 10)))[0]
    c = mpc.input(secint(random.randint(0, 10)))[0]

    # sid_data ist ein secint

    sid_data_gf = await mpc.gather(a)
    print("sid_data_gf ", sid_data_gf)
    sid_data_str = base64.encodebytes(pickle.dumps(sid_data_gf)).decode()
    print("sid_data_str ", sid_data_str, " type: ", type(sid_data_str))
    sid_data_restore = pickle.loads(base64.decodebytes(sid_data_str.encode('utf-8')))

    print("sid_data_restore ", sid_data_restore)

    a = sid_data_restore

    # und sid_data_str in json file geschrieben

    "type field"

    x = (a * b * c)

    # output würde veröffentlicht werden zB mittelwert
    # output am server
    # if node 0 dann lesen

    aa = await mpc.output(a)
    bb = await mpc.output(b)
    cc = await mpc.output(c)
    xx = await mpc.output(x)
    print(f"{aa} * {bb} * {cc} = {xx}")
    await mpc.shutdown()


mpc.run(main())