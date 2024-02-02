import json

# Sample list
l1 = [{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033814",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": ""
        },
        {
            "Caption": "Link to Person",
            "value": "10033814"
        },
        
    ],
    "SubData": []
},
{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033815",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": ""
        },
        {
            "Caption": "Link to Person",
            "value": "10033815"
        }
    ],
    "SubData": []
},
{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033814",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": "12"
        },
        {
            "Caption": "Link to Person",
            "value": "10033814"
        },
        
    ],
    "SubData": []
}
]



#dd = {}
# for record in l1:
#   key = record['KeyValue']
#   if key not in dd:
#     dd[key] = [record]
#   else:
#     dd[key].append(record)

# Create JSON files for each KeyValue group



import json

grouped_records = {"key1": {"name": "John", "age": 25},
                   "key2": {"name": "Alice", "age": 30},
                   "key1": {"name": "Bob", "age": 28}}

result = {}

for key_value, records in grouped_records.items():
    # Concatenate records with the same key
    result.setdefault(key_value, {}).update(records)

# Write the combined records to a single JSON file
with open("combined_records.json", "w") as json_file:
    json.dump(result, json_file, indent=2)







# Group records by KeyValue
grouped_records = {}
for record in l1:
    key_value = record["KeyValue"]
    if key_value not in grouped_records:
        grouped_records[key_value] = []
    grouped_records[key_value].append(record)

# Create JSON files for each KeyValue group
for key_value, records in grouped_records.items():
    file_name = f"{key_value}.json"
    with open(file_name, "w") as json_file:
        json.dump(records, json_file, indent=2)

print("JSON files created successfully.")



import json
import os

def convert_json_file(source_file_path, destination_file_path):
    try:
        with open(source_file_path, 'r') as source_file:
            data = json.load(source_file)
        # Write contents to the destination JSON file without the list operator
        with open(destination_file_path, 'w') as destination_file:
            for record in data:
                json.dump(record, destination_file, indent=2)
                destination_file.write('\n')
    except json.decoder.JSONDecodeError:
        print(f"Skipping invalid JSON file: {source_file_path}")

source_directory = '/AppDev/CEDL/etl/SrcFiles/lg/myevolve'

# Specify the directory where converted files will be saved
destination_directory = '/AppDev/CEDL/etl/SrcFiles/lg/myevolve'

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        source_file_path = os.path.join(source_directory, filename)
        destination_file_path = os.path.join(destination_directory, filename.replace('.json', '_converted.json'))
        convert_json_file(source_file_path, destination_file_path)

print("Conversion completed successfully.")

