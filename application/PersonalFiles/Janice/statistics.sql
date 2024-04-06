#Local Statistics 
#statistic #4 
select c.fname,c.lname, count (*) as count_reservation 
from client c inner join reserve r on c.clid = r.clid
where c.age < 30 and r.payment = 'credit card'
group by c.clid, c.fname, c.lname
order by count_reservation desc 
limit 5 

# statistic #7 
select rd.rtype, count(*) as reservations_total
from roomdescription rd natural inner join room natural inner join roomunavailable natural inner join reserve r 
group by rd.rtype 
order by rd.rtype

#Global Statistics 
#statistic #11 
select ch.cname count (*) as count_rooms
from chains ch natural inner join hotel natural inner join room r
group by ch.chid, cname
order by count_rooms asc
limit 3 