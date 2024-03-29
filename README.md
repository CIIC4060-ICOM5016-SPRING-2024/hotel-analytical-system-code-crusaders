# Hotel Analytical System Phase II

## Table of Contents
- [Objectives](#objectives)
- [Production Database](#production-Database)
- [Getting Started](#getting-started)
  - [Local setup](#local-setup)
  - [Instructions (Heroku)](#instructions-heroku)
- [How to use](#How-to-use)
- [Contributing](#contributing)

## Objectives
1. Understand the design, implementation and use of an application backed by a database system. 
2. Understand the use of table diagram for database application design. 
3. Gain experience by implementing applications using layers of increasing complexity and complex data structures.
4. Gain further experience with Web programming concepts including REST. 

## Production Database

To access production database on heroku, you will use the following credentials:
```bash
host=ec2-35-169-9-79.compute-1.amazonaws.com
username=edgviemrvgvubw
database=dcqjte9oo7j864
password=a625d1106cf9fe6ddcb87f11dc958726165b4cdb5563d46e56fba96f62cbbd1f

port=5432
URI=postgres://edgviemrvgvubw:a625d1106cf9fe6ddcb87f11dc958726165b4cdb5563d46e56fba96f62cbbd1f@ec2-35-169-9-79.compute-1.amazonaws.com:5432/dcqjte9oo7j864
```

To access the front-end of the application, use the following link:
```bash
rest_api_host=https://pdb-f386d9f3feff.herokuapp.com/
```

## Getting Started

### Local setup

### 1. Setup Docker Container
For this, you will need to have docker installed already in your machine. After having docker all setup
you will need the latest image of postgreSQL on a container. To get it, you will use the following command
on your terminal of preference:

```bash
docker pull postgres
```

To create and start running a new docker container with the postgres image in it run the following command:
```bash
docker run -d --name my-postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 postgres
```
For this the database created inside the container will have these credentials for the rest of the application use process.
These can change in the future but for project simplicity it will stay like this. For real production databases these we do not 
use dummy users and/or passwords.

### 2. Setup Application in container
Check if the container is running by typing:
```bash
docker ps
```
If the container is not running, consider checking previous steps or official docker documentation.

Next, you will need to install all dependencies that will make the application go functional.
For this you need to run the following command to enter the container using bash.
```bash
docker exec -it my-postgres-container bash
```

Once inside the container running bash, update the linux distribution version that the container is running on to the latest.
```bash
apt update
```

After updating, install the following dependencies
```bash
apt install -y python3 python3-pip git sqlite3 curl yay
```

Install heroku CLI for later production setup
```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh 
```

Check if all dependencies are installed by running individually:
```bash
python3 --version 
pip --version
git --version
sqlite3 --version 
curl --version 
yay --version 
heroku --version 
```
If one of these did not got installed inside the container, retry the commands or check official documentation
on each application.

### 3. Cloning repository and setting up application
For this part, you need to clone this repository in your local machine. After doing so, you need to copy the
cloned repository inside the docker container. Make sure the container still running.
This will copy the repository to the root directory inside the container.
```bash
docker cp <path of the cloned repository folder> my-postgres-container:/
```

To setup the application you will need a couple of python dependencies and a virtual enviroment. Luckly we got a
script to set this up ever time on a new repository. Inside the root directory inside the repository there is a file
named `setup_environment.sh`. By running this script, it will generate a virtual enviroment locally in your container and it will
install all python dependencies required for this application to work.

First, enter the container again
```bash
docker exec -it my-postgres-container bash
```
Enter the repository once inside the container
```bash
cd ./<repository name>
```
Give permision to the `setup_environment.sh` file to run.
```bash
chmod +x setup_environment.sh
```
Run the setup bash file to setup everything.
```bash
./setup_environment.sh
```

### 3. Create the tables
To load the data to the database to start testing, you will need to run the scripts related to transforming and
loading the data inside the `ETL/` directory. Similarly, for production database in heroku, you will use DataGrip or
vsCode for uploading the data.

Install python dependencies
```bash
# this is to have access to excel files
pip install pandas   
pip install openpyxl
```

If it throws you an error, you can setup a virtual enviroment for python
or you can just add the following flag after the pip install command
```bash

pip install -U pip
pip install pandas   --break-system-packages
pip install openpyxl --break-system-packages
pip install Flask
pip install flask-cors
pip install psycopg2-binary
```

### 5. Clone repository and move it into root's container
For this part you need to clone the repository and copy the folder to the root folder inside the container.
To clone the repository you need the link of this remote repository and write the following command:
```bash
git clone <your_github_repo_link_here>
```
You can clone the repository to where ever you want in your computer. After cloning the repository, you have to copy it into
the container. To do so, you will need to type the following command in your terminal (note that this is in your system's terminal
not your container's root).
```bash
docker cp <path of the cloned repository folder> my-postgres-container:/
```

### 6. Connect to PostgreSQL
For this you will need to be inside the container, to do this you can try step #4 again if you are out
from the container. Provide the port to which we can use to comunicate with the database, the user and
the database name all from localhost.
```bash
psql -h localhost -U myuser -d mydatabase -p 5432
```

## How to use

### How to extract the data that was provied? (Docker)

Enter the container's root directory
```bash
docker exec -it my-postgres-container bash
```
Once inside you can enter to the repository scripts folder using:
```bash
cd ./repository_name/ETL/scripts
```

The data to extract is located inside of `/data/unfiltered/` of this repository. 
Inside the `ETL` folder you can find a directory named scripts that contains the
`data_cleaner.py` script. This is used to extract the unfiltered data and transform
it to csv files. When the data is being transfered to the csv, it cleans the data
accordingly to have a valid csv as output.

To run this script you need to run the following inside the container:
```bash
python3 data_cleaner.py
```
If you get any errors, you'll need to check the dependencies if they were installed correctly.

To upload the data to the database, you will need to run the following script AFTER
running the previous script.
```bash
python3 mount_data.py
```

## Contributing
- Alfredo Soto
- Cesar Delgado
- Janice Figueroa
- Saúl Figueroa Gálvez