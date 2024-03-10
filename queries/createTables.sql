create table Chains (
    chid       serial primary key,   
    cname      varchar(50) not null,                  
    springmkup float, 
    fallmkup   float, 
    wintermkup float  
);

create table Hotel (
    hid   serial primary key,   
    chid  int references Chains(chid),                  
    hname varchar(50) not null, 
    hcity varchar(50) not null  
);

create table Employee (
    eid      serial primary key,           
    hid      int references Hotel(hid), 
    fname    varchar(64) not null,         
    lname    varchar(64) not null,                            
    position varchar(64) not null,                            
    salary   float                            
);

create table Login (
    lid      serial primary key,           
    eid      int references Employee(eid), 
    username varchar(64) not null,         
    password int                           
);

create table RoomDescription (
    rdid       serial primary key,   
    rname      varchar(64) not null, 
    rtype      varchar(64) not null, 
    capacity   int,                  
    ishandicap boolean                   
);

create table Room (
    rid    serial primary key, 
    hid    int references Hotel(hid),                
    rdid   int references RoomDescription(rdid),                
    rprice float       
);

create table RoomUnavailable (
    ruid      serial primary key, 
    rid       int references Room(rid),                
    startdate date not null,      
    enddate   date not null       
);

create table Client (
    clid       serial primary key,   
    fname      varchar(64) not null, 
    lname      varchar(64) not null, 
    age        int,                  
    memberyear int                   
);

create table Reserve (
    reid       serial primary key, 
    ruid       int references Room(rid),                
    clid       int references Client(clid),      
    total_cost float,    
    payment    varchar(64) not null,       
    guests     int       
);