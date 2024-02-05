import csv
import json


csv_data = []
csv_file_path = 'output1.csv'

csv_data = [] 
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Get the header from the first row
    header = next(csv_reader)
    # Iterate through rows and create dictionaries
    for row in csv_reader:
        row_dict = {header[i]: value for i, value in enumerate(row)}
        csv_data.append(row_dict)

grouped = {}
for record in csv_data:
  key = record['KeyValue']
  if key not in grouped:
    grouped[key] = [record]
  else:
    grouped[key].append(record)


form_lines = {}
for key, record in grouped.items():
    file_name = f"{key}.json"
    form_lines[key] = []  # Assuming form_lines is a dictionar
    for row in record:
        column_names = row.keys() 
        form_lines[key].extend([{"Caption": column, "value": row[column]} for column in column_names])

   
            
for key_value, row in form_lines.items():
    file_name = f"{key_value}.json"
    with open(file_name, "w") as json_file:
        json_data = {
            "AutomationKey": row['AutomationKey'],
            "FormMode": row['FormMode'],
            "KeyValue": row['KeyValue'],
            "FormLines": row,
            "SubData": []
        }
        json.dump(json_data, json_file, indent=4)
        json_file.write('\n')
