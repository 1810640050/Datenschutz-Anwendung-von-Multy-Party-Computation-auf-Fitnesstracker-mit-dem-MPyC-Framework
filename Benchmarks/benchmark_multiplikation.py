import math

from mpyc.runtime import mpc
import random
from time import time

secint = mpc.SecFxp()
n = 10**3

async def main():
    await mpc.start()
    st1 = time()
    a_lon_sec = mpc.input([secint(random.randint(0,100)) for _ in range(n)])[0]
    a_lat_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]
    b_lon_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]
    b_lat_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]

    await mpc.gather(a_lon_sec)
    await mpc.gather(a_lat_sec)
    await mpc.gather(b_lon_sec)
    await mpc.gather(b_lat_sec)
    end1 = time()
    print("Inputtime: ", end1-st1)

    sec_distances = []
    start = time()

    for i in range(n):
        dx = 71 * (a_lon_sec[i] - b_lon_sec[i])
        dy = 111 * (a_lat_sec[i] - b_lat_sec[i])
        erg = (mpc.pow(dx, 2) * mpc.pow(dy,2))
        sec_distances.append(erg)

        # uncomment to test latency with sequential execution:
        #await mpc.gather(sec_distances[i])

    await mpc.gather(sec_distances)
    end = time()
    criticaltime = end - start
    print("Executiontime: {0}".format(criticaltime))

    distances = await mpc.output(sec_distances)
    d = sum(map(math.sqrt, distances))
    print("Distance: {0} Executiontime: {1}".format(round(d), criticaltime))
    await mpc.shutdown()
mpc.run(main())