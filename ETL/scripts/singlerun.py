import subprocess

username = "myuser"
database = "mydatabase"
sql_file_path = "../queries/generaltester.sql"

psql_command = f"psql -U {username} -d {database}"

with open(sql_file_path, "r") as file:
    sql_commands = file.read()

try:
    subprocess.run(f"echo '{sql_commands}' | {psql_command}", shell=True, check=True)
    print("SQL commands executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing SQL commands:\n{e}")
