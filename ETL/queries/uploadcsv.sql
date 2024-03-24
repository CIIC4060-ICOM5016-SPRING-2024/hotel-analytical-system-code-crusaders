
-- This script is to upload the data to the docker container
-- You need to have uploaded the filtered data to the /data/filtered/ in root
-- if this is not done, the SQL query will not upload the data

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
        where ruid      is not null and
              rid       is not null and
              startdate is not null and
              enddate   is not null; 

copy Reserve(reid, ruid, clid, total_cost, payment, guests)                      
    from '/data/filtered/reserve.csv' delimiter ',' csv header;