import base64
import json


def _get_Path(filename):
	path = "storage/"
	PATH = path + filename
	return PATH

class GetIntOfStr():
	def __init__(self):
		pass
	def GetIntValue(str_value):
		sentence = ""
		ascii_vals = []
		for i in str_value:
			num = ord(i)
			sentence += str(f"{num:0=3d}")
		print("sentence ", sentence)
		sentence = ""

	def GetStrValue(int_value):
		return base64.encodebytes(int_value.decode())

class ReadWriteJson():
	def __init__(self):
		pass

	def create_jsonfile(filename, filemode, *args):
		path_to_file = _get_Path(filename)
		for i in args: # schleife notwendig, sonst wird eine liste statt dictionary gespeichert
			json_object = json.dumps(i, indent=4)
			with open(path_to_file, filemode) as file:
				file.write(json_object)

	def read_jsonfile(filename):
		path_to_file = _get_Path(filename)
		with open(path_to_file, 'r') as file:
			json_object = json.load(file)
			return json_object