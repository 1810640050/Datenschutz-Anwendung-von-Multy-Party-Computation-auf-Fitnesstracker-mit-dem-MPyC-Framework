from mpyc.runtime import mpc
import random
from time import time

secfxp = mpc.SecFxp()

async def main():
    await mpc.start()
    n = [random.randint(1,64000) for _ in range(20000)]

    ns = [secfxp(i) for i in n]
    vec = mpc.input(ns)[0]
    await mpc.gather(vec)

    start = time()
    erg = mpc.sum(vec)

    await mpc.gather(erg)
    end = time()
    criticaltime = end - start

    clear = await mpc.output(erg)
    print("Average Steps: {0} Execution Time: {1}".format(clear, criticaltime))
    await mpc.shutdown()
mpc.run(main())