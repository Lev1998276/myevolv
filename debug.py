file_path = 'output.csv'

with open(file_path, 'r') as csvfile:
	csv_reader = csv.DictReader(csvfile)
	headers = csv_reader.fieldnames
	data = [row for row in csv_reader]
	
	
	
def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
        data = [row for row in csv_reader]
    return headers, data
    
    
headers, data = read_csv(file_path)



for row in data:
  for x in headers:
      print(f"Caption:{x}, value:{row.get(x,'')}")


result = []
for row in data:
  for x in headers:
      temp = (f"Caption:{x}, value:{row.get(x,'')}")
      result.append(temp)


for row in data:
    print(row)
    form_line = [
        {"Caption": header, "value": row.get(header, "")} for header in headers
    ]
    json_data["FormLines"].append(form_line)
    
    
    
json_data = {
    "AutomationKey": 'tx_hx_hosp',
    "FormMode": 'ADD',
    "KeyValue": None,
    "FormLines": [],
    "SubData": []
}
    
    
    
# read csv file alternatively    
    
import csv

csv_file_path = 'output.csv'


def read_csv(file_path):
    result = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        for row in csv_reader:
            row_dict = {header[i]: value for i, value in enumerate(row)}
            result.append(row_dict)
    return result
    
data = read_csv('output.csv')


for eachrow in data:
    for idx, val in eachrow.items():
        print(idx, val)
        
        
formlines = []

for eachrow in data:
    for key, val in eachrow.items():
        temp = {"Caption": key, "value" : val}
        formlines.append(temp)
        