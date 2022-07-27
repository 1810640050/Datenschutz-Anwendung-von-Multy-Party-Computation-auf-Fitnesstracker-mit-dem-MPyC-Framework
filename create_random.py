import random
from mpyc.runtime import mpc
from json_inout import ReadWriteJson as rwj

ran_val = random.randint(0,100)

dict = {
    "ranval": ran_val
}
print(ran_val)
rwj.create_jsonfile("ran_val", 'w', dict)