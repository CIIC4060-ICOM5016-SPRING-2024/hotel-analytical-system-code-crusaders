import subprocess

# Set your PostgreSQL username, database name, and file path
username = "myuser"
database = "mydatabase"
sql_file_path = "../queries/createTables.sql"

# Construct the psql command
psql_command = f"psql -U {username} -d {database}"

# Read the SQL file content
with open(sql_file_path, "r") as file:
    sql_commands = file.read()

# Execute the SQL commands using subprocess
try:
    subprocess.run(f"echo '{sql_commands}' | {psql_command}", shell=True, check=True)
    print("SQL commands executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing SQL commands:\n{e}")
