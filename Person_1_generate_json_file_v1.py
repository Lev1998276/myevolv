
import csv
import json
import os 


def read_csv(csv_file_path, csv_file_mame):
    full_file_path= os.path.join(csv_file_path, csv_file_name)
    csv_data = []
    with open(full_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Get the header from the first row
        header = next(csv_reader)
        # Iterate through rows and create dictionaries
        for row in csv_reader:
            row_dict = {header[i]: value for i, value in enumerate(row)}
            csv_data.append(row_dict)
    # Clean up - remove the local copy of the CSV file
    #os.remove(local_file)
    return csv_data
    
    
    


def convert_row_to_json(row):
    column_names = row.keys()
    print(column_names)
    methodParameters =  [
        {"type": header, "value": row[header]} for header in row.keys() if header in ['IS_API_CALL']
    ]
    
    detail_data = [
                    {"type": header, "value": row[header]} for header in row.keys() if header not in ['AgencyIDNumber', 'FirstName', 'LastName', 'Gender', 'DateOfBirth']
                ]
                
    json_data = {
         "objPersonSearch":{
        "AgencyIDNumber": row['AgencyIDNumber'],
        "FirstName": row['FirstName'],
        "LastName": row['LastName'],
        "MiddleName": row['MiddleName'],
        "DateOfBirth": row['DateOfBirth'],
        "Gender": row['Gender'],
        "PeopleSystemID": row['PeopleSystemID'],
        "People3RDPartyID": row['People3RDPartyID'],
        "SocialSecurityNumber": row['SocialSecurityNumber'],
        "MedicaidNumber": row['MedicaidNumber'],
        "MatchOverride": False 
    },
    "objUpdatePerson": {
    "method": row['startautomation'],
    "methodParameters": methodParameters,
    "automationKey": row['VPIN_UP'],
    "version": "2.0",
    "detail": [
                {
                    "id": row['id'],
                    "foreignKeyID": row['foreignKeyID'],
                    "action": row['action'],
                    "keyValue": row['keyValue'],
                    "detail": detail_data,
                    "subData": []
                }
    
    ]
    }
    }
    return json_data
    
    
    
    

# Read the CSV file and extract data
csv_file_path = '/AppDev/CEDL/etl/SrcFiles/lg/person'
csv_file_name = 'person.csv'  
json_output_path = 'output.json'    

csv_data =  read_csv(csv_file_path, csv_file_name)

json_list = [convert_row_to_json(record) for record in csv_data if record]

for eachJson in json_list:
   print(json.dumps(eachJson, indent = 4))

