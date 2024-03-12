import subprocess

username = "myuser"
database = "mydatabase"
psql_command = f"psql -U {username} -d {database}"

createTables = "../queries/createTables.sql"
uploadcsv    = "../queries/uploadcsv.sql"

with open(createTables, "r") as file:
    sql_commands = file.read()
    
with open(uploadcsv, "r") as file:
    sql_commands += file.read()

try:
    subprocess.run(f"echo '{sql_commands}' | {psql_command}", shell=True, check=True)
    print("Mounted data successfuly.")
except subprocess.CalledProcessError as e:
    print(f"Error executing SQL commands:\n{e}")
