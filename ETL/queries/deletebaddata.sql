--Clean Room Unavailable
DELETE FROM room_unavailable WHERE ruid IS NULL OR trim(ruid) = '';
DELETE FROM room_unavailable WHERE rid IS NULL OR trim(rid) = '';
DELETE FROM room_unavailable WHERE start_date IS NULL OR trim(start_date) = '';
DELETE FROM room_unavailable WHERE end_date IS NULL OR trim(end_date) = '';
--Clean Chains
DELETE FROM chains WHERE chid IS NULL OR trim(chid) = '';
DELETE FROM chains WHERE cname IS NULL OR trim(cname) = '';
DELETE FROM chains WHERE springmkup IS NULL OR trim(springmkup) = '';
DELETE FROM chains WHERE summermkup IS NULL OR trim(summermkup) = '';
DELETE FROM chains WHERE fallmkup IS NULL OR trim(fallmkup) = '';
DELETE FROM chains WHERE wintermkup IS NULL OR trim(wintermkup) = '';
--Clean Client
DELETE FROM client WHERE clid IS NULL OR trim(clid) = '';
DELETE FROM client WHERE fname IS NULL OR trim(fname) = '';
DELETE FROM client WHERE lname IS NULL OR trim(lname) = '';
DELETE FROM client WHERE age IS NULL OR trim(age) = '';
DELETE FROM client WHERE memberyear IS NULL OR trim(memberyear) = '';
--Clean Employee
DELETE FROM employee WHERE eid IS NULL OR trim(eid) = '';
DELETE FROM employee WHERE hid IS NULL OR trim(hid) = '';
DELETE FROM employee WHERE fname IS NULL OR trim(lname) = '';
DELETE FROM employee WHERE lname IS NULL OR trim(lname) = '';
DELETE FROM employee WHERE age IS NULL OR trim(age) = '';
DELETE FROM employee WHERE position IS NULL OR trim(salary) = '';
--Clean Hotel
DELETE FROM hotel WHERE hid IS NULL OR trim(hid) = '';
DELETE FROM hotel WHERE chid IS NULL OR trim(chid) = '';
DELETE FROM hotel WHERE hname IS NULL OR trim(hname) = '';
DELETE FROM hotel WHERE hcity IS NULL OR trim(hcity) = '';
--Clean Login
DELETE FROM login WHERE lid IS NULL OR trim(lid) = '';
DELETE FROM login WHERE employeeid IS NULL OR trim(employeeid) = '';
DELETE FROM login WHERE user IS NULL OR trim(user) = '';
DELETE FROM login WHERE pass IS NULL OR trim(pass) = '';
--Clean Reserve
DELETE FROM reserve WHERE reid IS NULL OR trim(reid) = '';
DELETE FROM reserve WHERE ruid IS NULL OR trim(ruid) = '';
DELETE FROM reserve WHERE clid IS NULL OR trim(clid) = '';
DELETE FROM reserve WHERE total_cost IS NULL OR trim(total_cost) = '';
DELETE FROM reserve WHERE payment IS NULL OR trim(payment) = '';
DELETE FROM reserve WHERE guests IS NULL OR trim(guests) = '';
--Clean Room
DELETE FROM room WHERE rid IS NULL OR trim(rid) = '';
DELETE FROM room WHERE hid IS NULL OR trim(hid) = '';
DELETE FROM room WHERE rprice IS NULL OR trim(rprice) = '';
DELETE FROM room WHERE rdid IS NULL OR trim(rdid) = '';
--Clean Room Description
DELETE FROM roomdescription WHERE rdid IS NULL OR trim(rdid) = '';
DELETE FROM roomdescription WHERE rname IS NULL OR trim(rname) = '';
DELETE FROM roomdescription WHERE rtype IS NULL OR trim(rtype) = '';
DELETE FROM roomdescription WHERE capacity IS NULL OR trim(capacity) = '';
DELETE FROM roomdescription WHERE ishandicap IS NULL OR trim(ishandicap) = '';