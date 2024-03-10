import subprocess
import shutil

# Check if sqlite3 is installed
if shutil.which("sqlite3"):

    # Run the command to dump SQLite databases to SQL files
    subprocess.run(["sqlite3", "../unfiltered/rooms.db", ".dump"], stdout=open("../filtered/rooms.sql", "w"))
    subprocess.run(["sqlite3", "../unfiltered/reserve.db", ".dump"], stdout=open("../filtered/reserve.sql", "w"))
    subprocess.run(["sqlite3", "../unfiltered/reservations.db", ".dump"], stdout=open("../filtered/reservations.sql", "w"))
    
    print("Dumpped all 3 db files.")
else:
    print("Error: sqlite3 is not installed. Please install sqlite3 before running this script.")
