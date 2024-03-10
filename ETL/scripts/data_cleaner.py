import csv
import os
import glob
import json
import subprocess
import shutil
import pandas as pd

input_directory     = '../../data/unfiltered/'  # from repository
output_directory    = '../../../data/filtered/' # to root dir (outside repo)
output_directory_bk = '../../data/filtered/'    # from repository (for backup)

def write_to_csv(inPath, outPath, table_rows):
    # Open the output CSV file in write mode
    with open(outPath, 'w', newline='') as outfile:
        csvwriter = csv.writer(outfile)
        # Write each cleaned row to the new CSV file
        for cleaned_row in table_rows:
            csvwriter.writerow(cleaned_row)

    print(f'Data has been copied from "{inPath}" to "{outPath}" successfully.')
    pass

def read_from_csv(inPath):
    # Open the input CSV file in read mode
    with open(inPath, 'r') as infile:
        csvreader = csv.reader(infile)
        # Read and clean rows
        cleaned_rows = []
        for row in csvreader:
            if row:
                cleaned_rows.append(row)
    return cleaned_rows

def read_from_excel(inPath):
    # Read the Excel file into a DataFrame
    dataframe = pd.read_excel(inPath)
    dataframe = dataframe.dropna()
    columns = dataframe.columns.tolist()
    array_data = [columns] + dataframe.values.tolist()
    # Read and clean rows
    cleaned_rows = []
    for row in array_data:
        if row:
            cleaned_rows.append(row)
    return cleaned_rows

def read_from_json(inPath):
    # Open the JSON file in read mode
    with open(inPath, 'r') as jsonfile:
        data = json.load(jsonfile)
    # Extract column names
    columns = list(data[0].keys())
    # Flatten the JSON structure into a list of rows
    return [columns] + [[item.get(key, None) for key in columns] for item in data]

def scan_for_csvs(in_dir, out_dir, out_dir_bk):
    # Loop through all CSV files in the input directory
    for input_path in glob.glob(os.path.join(in_dir, '*.csv')):
        # Extract the file name from the file path
        filename = os.path.splitext(os.path.basename(input_path))[0]
        # Generate the output CSV path based on the input file
        output_path = os.path.join(out_dir, f'{filename}.csv')
        output_path_bk = os.path.join(out_dir_bk, f'{filename}.csv')

        table_rows = read_from_csv(input_path)

        write_to_csv(input_path, output_path,    table_rows) # write to root
        write_to_csv(input_path, output_path_bk, table_rows) # backup in repo
    pass

def scan_for_excels(in_dir, out_dir, out_dir_bk):
    # Loop through all EXCEL files in the input directory
    for input_path in glob.glob(os.path.join(in_dir, '*.xlsx')):
        # Extract the file name from the file path
        filename = os.path.splitext(os.path.basename(input_path))[0]
        # Generate the output EXCEL path based on the input file
        output_path = os.path.join(out_dir, f'{filename}.csv')
        output_path_bk = os.path.join(out_dir_bk, f'{filename}.csv')

        table_rows = read_from_excel(input_path)

        write_to_csv(input_path, output_path,    table_rows) # write to root
        write_to_csv(input_path, output_path_bk, table_rows) # backup in repo
    pass

def scan_for_jsons(in_dir, out_dir, out_dir_bk):
    # Loop through all JSON files in the input directory
    for input_path in glob.glob(os.path.join(in_dir, '*.json')):
        # Extract the file name from the file path
        filename = os.path.splitext(os.path.basename(input_path))[0]
        # Generate the output JSON path based on the input file
        output_path = os.path.join(out_dir, f'{filename}.csv')
        output_path_bk = os.path.join(out_dir_bk, f'{filename}.csv')

        table_rows = read_from_json(input_path)
        
        write_to_csv(input_path, output_path,    table_rows) # write to root
        write_to_csv(input_path, output_path_bk, table_rows) # backup in repo
    pass

def dbfiles_to_csv(database_filename, database_tablename, in_dir, out_dir, out_dir_bk):
    # Check if sqlite3 is installed
    if not shutil.which("sqlite3"):
        print("Error: sqlite3 is not installed. Please install sqlite3 before running this script.")
        pass
    
    subprocess.run(
        [
            "sqlite3",
            f"{in_dir}{database_filename}.db",
            ".mode csv",
            f".output {out_dir}{database_tablename}.csv",
            ".headers on",
            f"SELECT * FROM {database_tablename};", ".quit"
        ]
    )
    subprocess.run(
        [
            "sqlite3",
            f"{in_dir}{database_filename}.db",
            ".mode csv",
            f".output {out_dir_bk}{database_tablename}.csv",
            ".headers on",
            f"SELECT * FROM {database_tablename};", ".quit"
        ]
    )
    pass

# Always create the output directory before cleaning data
os.makedirs(output_directory, exist_ok=True)

scan_for_csvs(input_directory, output_directory, output_directory_bk)
scan_for_excels(input_directory, output_directory, output_directory_bk)
scan_for_jsons(input_directory, output_directory, output_directory_bk)

dbfiles_to_csv("rooms", "room", input_directory, output_directory, output_directory_bk)
dbfiles_to_csv("reservations", "reserve", input_directory, output_directory, output_directory_bk)