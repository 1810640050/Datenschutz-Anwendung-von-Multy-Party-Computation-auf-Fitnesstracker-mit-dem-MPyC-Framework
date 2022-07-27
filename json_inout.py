import json

class ReadWriteJson():
	def __init__(self):
		pass

	def create_jsonfile(filename, filemode, *args):
		for i in args: # schleife notwendig, sonst wird eine liste statt dictionary gespeichert
			json_object = json.dumps(i, indent=4)
			with open(filename, filemode) as file:
				file.write(json_object)

	def read_jsonfile(filename):
		with open(filename, 'r') as file:
			json_object = json.load(file)
			#print(type(json_object))
			return json_object
