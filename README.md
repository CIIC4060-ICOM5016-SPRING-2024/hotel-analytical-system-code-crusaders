# Hotel Analytical System

## Table of Contents
- [Objectives](#objectives)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Instructions](#instructions)
- [Contributing](#contributing)

## Objectives
1. Understand the design, implementation and use of an application backed by a database system. 
2. Understand the use of table diagram for database application design.  
3. Gain experience by implementing applications using layers of increasing complexity and complex data structures. 
4. Understand the design, implementation and use of a data pipeline using the ETL concept. 
5. Gain overall knowledge with OLAP systems.

## Getting Started
### Prerequisites
Before starting, docker must be instaleled on your machine. Once docker is installed you can pull the default Postgres container from docker itself through the terminal.
```
docker pull postgres
```

### Instructions

### 1. Create and run a new docker PostgreSQL container
You can run this in the terminal or in a executable bash file.

for executable bash file:
```bash
docker run -d                     \
  --name my-postgres-container    \
  -e POSTGRES_USER=myuser         \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase       \
  -p 5432:5432                    \
  postgres
```
in terminal:
```bash
docker run -d --name my-postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 postgres
```

### 2. Verify the container is running
Check if the container is running, if not check previous steps or official docker documentation
```bash
docker ps
```

### 3. Connect to PostgreSQL
Provide the port to which we can use to comunicate with the database, the user and the database name all from localhost.
```bash
psql -h localhost -U myuser -d mydatabase -p 5432
```

## Contributing
