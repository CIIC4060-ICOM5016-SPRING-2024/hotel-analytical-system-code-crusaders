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