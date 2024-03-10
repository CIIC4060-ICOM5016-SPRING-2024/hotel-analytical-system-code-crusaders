-- Copy the data from the csv to client table
copy Client(clid, fname, lname, age, memberyear)                         
    from '/data/filtered/client.csv' delimiter ',' csv header;           
                                                                         
-- -- Copy the data from the csv to hotel table
copy Hotel(hid, chid, hname, hcity)                                      
    from '/data/filtered/hotel.csv' delimiter ',' csv header;            
                                                                         
-- -- Copy the data from the csv to room unavaliable table
copy RoomUnavailable(ruid, rid, startdate, enddate)                      
    from '/data/filtered/room_unavailable.csv' delimiter ',' csv header   
        where ruid      is not null and
              rid       is not null and
              startdate is not null and
              enddate   is not null;