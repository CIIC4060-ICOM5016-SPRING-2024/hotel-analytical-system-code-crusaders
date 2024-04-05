select rid, sum((enddate - startdate)) as datediff
from room natural inner join roomunavailable
where hid = (select hid from login natural inner join employee natural inner join hotel natural inner join chains where lid = 1)
group by rid
order by datediff desc
limit 3;

select payment, cast((count(*) * 100) as decimal(20,2)) / (select count(*) from reserve)  as percentage
from reserve
group by payment;

select hname, count(*) as reservations
from hotel natural inner join room natural inner join roomunavailable natural inner join reserve
group by hname
order by reservations desc
limit ( 0.1 * (select count( distinct hname)
from hotel natural inner join room natural inner join roomunavailable natural inner join reserve));

select rid,cast(cast((guests) as decimal) / (capacity) as decimal(20,3)) as ratio from
(select rid, guests, capacity
from roomdescription natural inner join room natural inner join roomunavailable natural inner join reserve
group by rid,guests,capacity
order by rid)
order by ratio asc
limit 3;
