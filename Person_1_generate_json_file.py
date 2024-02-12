
import csv
import json

# Read the CSV file and extract data
csv_file_path = 'person.csv'  # Replace with the actual path to your CSV file
json_output_path = 'output.json'     # Replace with the desired output path for JSON file

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
   
    # Extract data for objPersonSearch
    obj_person_search_data = {}
    for row in csv_reader:
        obj_person_search_data = {
            AgencyIDNumber: row['AgencyIDNumber'],
            FirstName: row['FirstName'],
            LastName: row['LastName'],
            MiddleName: row['MiddleName'],
            DateOfBirth: row['DateOfBirth'],
            Gender: row['Gender'],
            PeopleSystemID: row['PeopleSystemID'],
            People3RDPartyID: row['People3RDPartyID'],
            SocialSecurityNumber: row['SocialSecurityNumber'],
            MedicaidNumber: row['MedicaidNumber'],
            MatchOverride: false  # Assuming MatchOverride is always false
        }
        break  # Assuming there is only one row for objPersonSearch

    # Extract data for objUpdatePerson
    obj_update_person_data = {
        method: 'startautomation',
        methodParameters: [
            {type: header, value: row[header]} for header in row.keys() if header not in ['AgencyIDNumber', 'FirstName', 'LastName', 'Gender', 'DateOfBirth']
        ],
        automationKey: row['VPIN_UP'],
        version: 2.0,
        detail: [
            {
                id: None,
                foreignKeyID: None,
                action: row['action'],
                keyValue: row['AgencyIDNumber'],
                data: [
                    {type: header, value: row[header]} for header in row.keys() if header not in ['AgencyIDNumber', 'FirstName', 'LastName', 'Gender', 'DateOfBirth']
                ],
                subData: []
            }
        ]
    }

# Construct the final JSON structure
final_json = {
    objPersonSearch: obj_person_search_data,
    objUpdatePerson: obj_update_person_data
}

# Write the JSON to a file
with open(json_output_path, 'w') as json_file:
    json.dump(final_json, json_file, indent=2)

print("JSON file has been created successfully")