import random
from mpyc.runtime import mpc
from json_inout import ReadWriteJson as rwj

ran_val = random.randint(0,100)

dict = {
    "value": ran_val
}
print(dict)
rwj.create_jsonfile("input_values.json", 'w', dict)

