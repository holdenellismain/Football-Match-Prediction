import pandas
import csv
from os import path

def append_csv(df, out_path):
    file_exists = path.isfile(out_path)
    if file_exists:
        df.to_csv(out_path, mode='a', index=False, header=False)
    else:
        df.to_csv(out_path, index=False, header=True)
    print("DF written to file")

def append_row(file_path, dict_data):
    # Check if the file exists
    file_exists = path.isfile(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        # Get the fieldnames from the dictionary keys
        fieldnames = dict_data.keys()
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(dict_data)