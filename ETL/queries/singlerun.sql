create table if not exists Client (
    clid       serial primary key,   
    fname      varchar(64) not null, 
    lname      varchar(64) not null, 
    age        int,                  
    memberyear int                   
);

create table if not exists Chains (
    chid       serial primary key,   
    cname      varchar(50) not null,                  
    springmkup float, 
    summermkup float, 
    fallmkup   float, 
    wintermkup float  
);

create table if not exists RoomDescription (
    rdid       serial primary key,   
    rname      varchar(64) not null, 
    rtype      varchar(64) not null, 
    capacity   int,                  
    ishandicap boolean                   
);

create table if not exists Hotel (
    hid   serial primary key,   
    chid  int references Chains(chid),                  
    hname varchar(50) not null, 
    hcity varchar(50) not null  
);

create table if not exists Employee (
    eid      serial primary key,           
    hid      int references Hotel(hid), 
    fname    varchar(64) not null,         
    lname    varchar(64) not null,                            
    age      int,                            
    position varchar(64) not null,                            
    salary   float                            
);

create table if not exists Login (
    lid      serial primary key,           
    eid      int references Employee(eid), 
    username varchar(64) not null,         
    password varchar(64) not null                           
);

create table if not exists Room (
    rid    serial primary key, 
    hid    int references Hotel(hid),                
    rdid   int references RoomDescription(rdid),                
    rprice float       
);

create table if not exists RoomUnavailable (
    ruid      serial primary key, 
    rid       int references Room(rid),                
    startdate date not null,      
    enddate   date not null       
);

create table if not exists Reserve (
    reid       serial primary key, 
    ruid       int references RoomUnavailable(ruid),                
    clid       int references Client(clid),      
    total_cost float,    
    payment    varchar(64) not null,       
    guests     int       
);

copy Client(clid, fname, lname, age, memberyear)                         
    from '/data/filtered/client.csv' delimiter ',' csv header;           

-- Create a temporary table to hold the data
create temp table temp_chains as
    select
        chid::float, -- cast chid to float
        cname,
        springmkup,
        summermkup,
        fallmkup,  
        wintermkup 
    from Chains;

copy temp_chains(chid, cname, springmkup, summermkup, fallmkup, wintermkup)                         
    from '/data/filtered/chain.csv' delimiter ',' csv header; 

-- Insert into the target table from the temporary table
insert into Chains(chid, cname, springmkup, summermkup, fallmkup, wintermkup)
    select 
        chid::int,  -- cast chid back to int
        cname,
        springmkup,
        summermkup,
        fallmkup,
        wintermkup
    from temp_chains;

drop table temp_chains;

copy RoomDescription(rdid, rname, rtype, capacity, ishandicap)
    from '/data/filtered/roomdetails.csv' delimiter ',' csv header;

copy Hotel(hid, chid, hname, hcity)                                      
    from '/data/filtered/hotel.csv' delimiter ',' csv header;            

copy Employee(eid, hid, fname, lname, age, salary, position)
    from '/data/filtered/employee.csv' delimiter ',' csv header;   

copy Login(lid, eid, username, password)
    from '/data/filtered/login.csv' delimiter ',' csv header;  

copy Room(rid, hid, rdid, rprice)
    from '/data/filtered/room.csv' delimiter ',' csv header;  

copy RoomUnavailable(ruid, rid, startdate, enddate)                      
    from '/data/filtered/room_unavailable.csv' delimiter ',' csv header   
        where 
            ruid      is not null and
            rid       is not null and
            startdate is not null and
            enddate   is not null; 

copy Reserve(reid, ruid, clid, total_cost, payment, guests)                      
    from '/data/filtered/reserve.csv' delimiter ',' csv header;

drop table if exists Client          cascade;
drop table if exists Chains          cascade;
drop table if exists RoomDescription cascade;
drop table if exists Hotel           cascade;
drop table if exists Employee        cascade;
drop table if exists Login           cascade;
drop table if exists Room            cascade;
drop table if exists RoomUnavailable cascade;
drop table if exists Reserve         cascade;