import os
import subprocess

username = "myuser"
database = "mydatabase"
psql_command = f"psql -U {username} -d {database}"

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

try:
    # Construct the path to the SQL file
    sql_file_path = os.path.join(script_dir, "../queries/createTables.sql")

    with open(sql_file_path, "r") as file:
        sql_command = file.read()
        subprocess.run(f"echo '{sql_command}' | {psql_command}", shell=True, check=True)

    # Construct the path to the SQL file
    sql_file_path = os.path.join(script_dir, "../queries/uploadcsv.sql")

    with open(sql_file_path, "r") as file:
        sql_command = file.read()
        subprocess.run(f"echo '{sql_command}' | {psql_command}", shell=True, check=True)

    print("Mounted data successfuly.")
except subprocess.CalledProcessError as e:
    print(f"Error executing SQL commands:\n{e}")
