import base64
import csv
import json
from datetime import date, time, datetime

def _get_Path(filename):
	PATH = "storage/"+filename
	return PATH

class ComputeDates():
	def __init__(self):
		pass
	def get_Timestamp_of_String(timestring):
		d = datetime.strptime(timestring, "%Y:%m:%d")
		return int(round(datetime.timestamp(d)))

	def get_Datetime_of_Timestamp(stamp):
		return datetime.fromtimestamp(stamp)

class GetIntOfStr():
	def __init__(self):
		pass
	def get_Int_Value(str_value):
		sentence = ""
		ascii_vals = []
		for i in str_value:
			num = ord(i)
			sentence += str(f"{num:0=3d}")
		print("sentence ", sentence)
		sentence = ""

	def get_String_Value(int_value):
		return base64.encodebytes(int_value.decode())

class ReadWriteJson():
	def __init__(self):
		pass

	def create_Json_File(filename, filemode, *args):
		path_to_file = "storage/"+filename  #_get_Path(filename)
		for i in args: # schleife notwendig, sonst wird eine liste statt dictionary gespeichert
			json_object = json.dumps(i, indent=4)
			with open(path_to_file, filemode) as file:
				file.write(json_object)

	def read_Json_File(filename):
		path_to_file = _get_Path(filename)
		with open(path_to_file, 'r') as file:
			json_object = json.load(file)
			return json_object


class ReadWriteCSV:
	def __init__(self):
		pass
	def get_CSV_as_List(filename):
		list = []
		path_to_file = _get_Path(filename)
		with open(path_to_file, 'r', newline='') as file:
			csv_file = csv.reader(file, delimiter=',')
			for line in csv_file:
				list.append(line)
		return list

	def WriteCSV(filename, filemode, *args):
		path_to_file = _get_Path(filename)
		for line in args:
			with open(path_to_file, filemode, encoding='UTF-8', newline='') as file:
				writer = csv.writer(file)
				writer.writerow(line)