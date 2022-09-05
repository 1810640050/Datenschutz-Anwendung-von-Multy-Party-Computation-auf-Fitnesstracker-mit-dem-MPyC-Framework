import math

from mpyc.runtime import mpc
import random
from time import time

secint = mpc.SecInt()
n = 10**3

async def main():
    await mpc.start()
    a_lon_sec = mpc.input([secint(random.randint(0,100)) for _ in range(n)])[0]
    a_lat_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]
    b_lon_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]
    b_lat_sec = mpc.input([secint(random.randint(0, 100)) for _ in range(n)])[0]

    await mpc.gather(a_lon_sec)
    await mpc.gather(a_lat_sec)
    await mpc.gather(b_lon_sec)
    await mpc.gather(b_lat_sec)

    sec_distances = []
    start = time()
    # Multiplikation
    for i in range(n):
        dx = 71 * (a_lon_sec[i] - b_lon_sec[i])
        dy = 111 * (a_lat_sec[i] - b_lat_sec[i])
        sec_distances.append(mpc.pow(dx, 2) + mpc.pow(dy,2))

        # uncomment to test latency with sequential execution:
        #await mpc.gather(sec_distances[i])

    end = time()
    criticaltime = end - start

    distances = await mpc.output(sec_distances)
    d = sum(map(math.sqrt, distances))
    print("Distance: {0} Executiontime: {1}".format(round(d), criticaltime))
    await mpc.shutdown()
mpc.run(main())