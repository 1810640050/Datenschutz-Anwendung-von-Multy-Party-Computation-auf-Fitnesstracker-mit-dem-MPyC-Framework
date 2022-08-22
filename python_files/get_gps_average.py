from mpyc.runtime import mpc
from math import sqrt

secflt = mpc.SecFlt()


class Point():
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Distance():
    def __init__(self, point_a , point_b):
        self.point_a = point_a
        self.point_b = point_b
        self.distance = None

    def calc_distance(self):
        lat1 = self.point_a.latitude
        lon1 = self.point_a.longitude
        lat2 = self.point_b.latitude
        lon2 = self.point_b.longitude

        # "Die Konstante 111.3 ist dabei der Abstand zwischen zwei Breitenkreisen in km
        # und 71.5 der durchschnittliche Abstand zwischen zwei Längenkreisen in unseren Breiten."
        # https://www.kompf.de/gps/distcalc.html
        dx = 71.5 * (lon1 - lon2)
        dy = 111.3 * (lat1 - lat2)
        base = (dx * dx + dy * dy)
        return base


async def main():
    await mpc.start()

    # TODO Loop through pointlist
    # TODO Safe an Calc results

    p1 = Point(None, None)
    p2 = Point(None, None)

    p1.latitude = secflt(52.2296756)
    p1.longitude = secflt(21.0122287)
    p2.latitude = secflt(52.406374)
    p2.longitude = secflt(16.9251681)

    dis1 = Distance(p1, p2)

    # sqrt bzw pow wird für secfloat oder float nicht unterstützt:
    # Positionsdaten bleiben geheim, die jeweiligen distanzen sind jedoch bekannt
    clear_base = await mpc.output(dis1.calc_distance())
    erg = sqrt(clear_base)
    print("Distance: {0} meters ".format(erg * 1000))

    await mpc.shutdown()

mpc.run(main())