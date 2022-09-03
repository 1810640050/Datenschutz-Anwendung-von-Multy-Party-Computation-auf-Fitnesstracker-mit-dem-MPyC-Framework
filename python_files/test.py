from mpyc.runtime import mpc
import random
from time import time

secfxp = mpc.SecFxp()

async def main():
    await mpc.start()
    a = mpc.input(secfxp(random.randint(1000, 64000)))[0]
    b = mpc.input(secfxp(random.randint(1000, 64000)))[0]
    print("a ", a)
    start = time()
    erg = a * a + b * b
    await mpc.gather(erg)
    end = time()
    criticaltime = end - start
    aa = await mpc.output(erg)
    print("Ergebnis: ", aa, " Executiontime: ", criticaltime)
    await mpc.shutdown()

mpc.run(main())