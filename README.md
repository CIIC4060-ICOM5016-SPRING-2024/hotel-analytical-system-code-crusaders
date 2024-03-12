# Hotel Analytical System

## Table of Contents
- [Objectives](#objectives)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Instructions](#instructions)
- [How to use](#How-to-use)
- [Contributing](#contributing)

## Objectives
1. Understand the design, implementation and use of an application backed by a database system. 
2. Understand the use of table diagram for database application design.  
3. Gain experience by implementing applications using layers of increasing complexity and complex data structures. 
4. Understand the design, implementation and use of a data pipeline using the ETL concept. 
5. Gain overall knowledge with OLAP systems.

## Getting Started
### Prerequisites
For testing you will need docker to run containers with a PostgreSQL image. Here we can test all queries and
extract, modify and load the data provided to the database. For production, you will need heroku all set up.
Here it will run the PostgreSQL database with the final results and queries.

In order to get the postgres image for docker, you can run the following command in your terminal. For this
you will need to have docker allready installed in your local machine.
```
docker pull postgres
```

### Instructions

### 1. Create and run a new docker PostgreSQL container

Running the following command in the terminal will create and run a container with postgres within it.
```bash
docker run -d --name my-postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 postgres
```

This database will have default user and credentials as showned in the command above. For purposes of this project the credentials
will be the following:
```bash
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
```

### 2. Verify the container is running
Check if the container is running, if not check previous steps or official docker documentation
```bash
docker ps
```

### 3. Enter the container and update/install dependencies
To install all dependencies to make everything functional, first you have to enter the container
```bash
docker exec -it my-postgres-container bash
```

Once inside the container running bash, update the debian version that the container is running on
```bash
apt update
```

After updating, install the following dependencies
```bash
apt install -y python3 python3-pip git sqlite3 
```

Check if installation was successfull
```bash
python3 --version 
pip --version
git --version
sqlite3 --version 
```

Install python dependencies
```bash
# this is to have access to excel files
pip install pandas   
pip install openpyxl
```

If it throws you an error, you can setup a virtual enviroment for python
or you can just add the following flag after the pip install command
```bash
pip install pandas   --break-system-packages
pip install openpyxl --break-system-packages
```

### 4. Clone repository on root
For this part you need to clone the repository to the root folder inside the container.
You should be inside root when you enter the container to install all dependencies. To clone
the repository you need the link of this remote repository and write the following command:
```bash
git clone <your_github_repo_link_here>
```

In case of this not working inside the container, you will need to exit back to your local machine's terminal
and clone the repository somewhere in your computer. After doing so, you will need to copy the cloned repository folder
into the `root` location inside the container.

try this inside your local machine, preferably in your desktop.
```bash
git clone <your_github_repo_link_here>
```
Then try the following command to copy the cloned repository to the root's directory inside the container.
```bash
docker cp <path of the cloned repository folder> my-postgres-container:/
```

### 5. Connect to PostgreSQL
For this you will need to be inside the container, to do this you can try step #3 again if you are out
from the container. Provide the port to which we can use to comunicate with the database, the user and
the database name all from localhost.
```bash
psql -h localhost -U myuser -d mydatabase -p 5432
```

## How to use

### How to extract the data that was provied?

The data to extract is located inside of `/data/unfiltered/` of this repository. Here is all
the data that needs to be extracted. Inside the `ETL` folder you can find a directory named
scripts that contains the `data_cleaner.py` script. This is used to extract the unfiltered data
and transform it to csv files. When the data is being transfered to the csv, it cleans the data
accordingly to have a valid csv as output, meaning that the output csv must not contain blank
lines.

To run this script you need to run the followings:
```bash
# to move inside the scripts folder
cd ./repository/ETL/scripts

# to execute the script
python3 data_cleaner.py
```
If you get any errors, you'll need to check the dependencies if they were installed correctly.


## Contributing
- Alfredo Soto
- Cesar Delgado
- Janice Figueroa
- Saúl Figueroa Gálvez