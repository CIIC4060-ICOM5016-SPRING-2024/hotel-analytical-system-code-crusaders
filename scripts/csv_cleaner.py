import csv
import os
import glob

# Specify the path to your input and output CSV directories
input_csv_directory    = '../data/unfiltered/' # from repository
input_csv_directory_bk = '../data/filtered/'   # from repository (for backup)
output_csv_directory   = '/data/filtered/'     # to root dir

os.makedirs(output_csv_directory, exist_ok=True)

def write_to_csv(outPath, table_rows):
    # Open the output CSV file in write mode
    with open(outPath, 'w', newline='') as outfile:
        csvwriter = csv.writer(outfile)
        csvwriter.writerow(header)

        # Write each cleaned row to the new CSV file
        for cleaned_row in table_rows:
            csvwriter.writerow(cleaned_row)

# Loop through all CSV files in the input directory
for input_csv_path in glob.glob(os.path.join(input_csv_directory, '*.csv')):
    # Generate the output CSV path based on the input file
    output_csv_path = os.path.join(output_csv_directory, os.path.basename(input_csv_path))
    output_csv_path_bk = os.path.join(input_csv_directory_bk, os.path.basename(input_csv_path))

    # Open the input CSV file in read mode
    with open(input_csv_path, 'r') as infile:
        csvreader = csv.reader(infile)

        # Read the header
        header = next(csvreader)

        # Read and clean rows
        cleaned_rows = []
        for row in csvreader:
            if row:
                cleaned_rows.append(row)

    write_to_csv(output_csv_path,    cleaned_rows) # write to root
    write_to_csv(output_csv_path_bk, cleaned_rows) # backup in repo

    print(f'Data has been copied from "{input_csv_path}" to "{output_csv_path}" successfully.')
