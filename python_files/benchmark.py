from mpyc.runtime import mpc
import random
from time import time

secfxp = mpc.SecFxp()

async def main():
    await mpc.start()
    n = [random.randint(1,64000) for _ in range(100)]
    print(sum(n))
    #zwerg = 1
    #for i in n:
    #    zwerg *= i
    #print(zwerg)
    ns = [secfxp(i) for i in n]
    vec = mpc.input(ns)[0]

    start = time()
    # Addition
    erg = mpc.sum(vec)

    # Multiplikation
    #erg = 1
    #for i in vec:
    #    erg *= i

    await mpc.gather(erg)
    end = time()
    criticaltime = end - start

    clear = await mpc.output(erg)
    print([clear, criticaltime])
    await mpc.shutdown()
mpc.run(main())