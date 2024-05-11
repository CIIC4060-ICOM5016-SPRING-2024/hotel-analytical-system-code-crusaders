from config.Database import Database

class StatisticsDAO:
    
    def __init__(self):
        Database().create_function(
            """
            create or replace function get_mem_discount(years_of_membership int)
            returns decimal as $$
            declare
                discount decimal;
            begin
                case
                    when years_of_membership >= 1  and years_of_membership <= 4  then
                        discount := 0.02; -- 2%
                    when years_of_membership >= 5  and years_of_membership <= 9  then
                        discount := 0.05; -- 5%
                    when years_of_membership >= 10 and years_of_membership <= 14 then
                        discount := 0.08; -- 8%
                    when years_of_membership >= 15 then
                        discount := 0.12; -- 12%
                    else
                        discount := 0; -- No discount for less than 1 year of membership
                end case;
                
                return discount;
            end;
            $$ language plpgsql;
            """
        )

    #
    #
    # LOCAL STATISTICS
    #
    #

    def get_Handicaproom(self, id):
        result = Database().querySelectFrom(
            """
            select  rname, rtype,
                    count(*) as reservation_count
                from roomdescription
                    natural inner join room
                    natural inner join reserve
                    natural inner join roomunavailable
                where
                    hid = %s and
                    ishandicap = true
            group by rdid
            order by reservation_count desc
            limit 5;
            """,
            (id,)
        )
        return result
    
    def get_LeastReserve(self, id):
        result = Database().querySelectFrom(
            """
            select  rid,
                    sum(enddate - startdate) as datediff
                from room
                    natural inner join roomunavailable
                where
                    hid = %s
            group by rid
            order by datediff asc
            limit 3;
            """,
            (id,)
        )
        return result

    def get_MostCreditCard(self, id):
        result = Database().querySelectFrom(
            """
            select  fname || ' ' || lname as full_name,
                    count (*) as count_reservation 
                from client
                    natural inner join reserve
                    natural inner join roomunavailable
                    natural inner join room
                where age < 30 and
                    payment = 'credit card' and
                    hid = %s
            group by clid
            order by count_reservation desc 
            limit 5;
            """,
            (id,)
        )
        return result

    def get_HighestPaid(self, id):
        result = Database().querySelectFrom(
            """
            select  eid,
                    fname || ' ' || lname as full_name,
                    salary 
                from employee
                where
                    hid = %s and
                    position = 'Regular' 
            order by salary desc
            limit 3;
            """,
            (id,)
        )
        return result

    def get_MostDiscount(self, id):
        result = Database().querySelectFrom(
            """
            select  fname || ' ' || lname  as full_name,
                    sum(total_cost * get_mem_discount(memberyear)) as discount
                from client
                    natural inner join reserve
                    natural inner join roomunavailable
                    natural inner join room
                    natural inner join hotel
                where
                    hid = %s
            group by clid
            order by discount desc
            limit 5;
            """,
            (id,)
        )
        return result
    
    def get_RoomType(self, id):
        result = Database().querySelectFrom(
            """
            select rtype, count(*) as reservations_total
                from roomdescription
                    natural inner join room
                    natural inner join roomunavailable
                    natural inner join reserve 
                where
                    hid = %s
            group by rtype 
            order by rtype;
            """,
            (id,)
        )
        return result
    
    def get_LeastGuests(self, id):
        result = Database().querySelectFrom(
            """
            select  rid,
                    cast(cast((guests) as decimal) / (capacity) as decimal(20,3)) as ratio
                from room
                    natural inner join roomdescription
                    natural inner join roomunavailable
                    natural inner join reserve
                where
                    hid = %s
            group by rid, guests, capacity
            order by ratio asc
            limit 3;
            """,
            (id,)
        )
        return result

    #
    #
    # GLOBAL STATISTICS
    #
    #

    def get_MostRevenue(self):
        result = Database().querySelectFrom(
            """
            select  chid, cname,
                    sum(total_cost) as total_revenue
                from chains
                    natural inner join hotel
                    natural inner join room
                    natural inner join roomunavailable
                    natural inner join reserve
            group by chid
            order by total_revenue desc
            limit 3;
            """, ()
        )
        return result

    def get_PaymentMethod(self):
        result = Database().querySelectFrom(
            """
            select  payment,
                    cast((count(*) * 100) as decimal(20,2)) / (select count(*) from reserve) as percentage
                from reserve
            group by payment;
            """, ()
        )
        return result

    def get_LeastRooms(self):
        result = Database().querySelectFrom(
            """
            select cname, count(*) as count_rooms
                from chains
                    natural inner join hotel
                    natural inner join room
            group by chid, cname
            order by count_rooms asc
            limit 3;
            """, ()
        )
        return result

    def get_MostCapacity(self):
        result = Database().querySelectFrom(
            """
            select hname, sum(capacity) as total_capacity
                from hotel 
                    natural inner join room
                    natural inner join roomdescription
            group by hid, hname
            order by total_capacity desc
            limit 5;
            """, ()
        )
        return result

    def get_MostReservation(self):
        result = Database().querySelectFrom(
            """
            with custom_limiter as (
                select count(distinct hname) as limiter
                    from hotel
                        natural inner join room
                        natural inner join roomunavailable
                        natural inner join reserve
            )

            select hname, count(*) as reservations
                from hotel
                    natural inner join room
                    natural inner join roomunavailable
                    natural inner join reserve
            group by hname
            order by reservations desc
            limit 0.1 * (select limiter from custom_limiter);
            """, ()
        )
        return result

    def get_MostProfitMonth(self):
        result = Database().querySelectFrom(
            """
            with reservation_by_month as 
            (
                select  chid,
                        cname as name,
                        extract(month from startdate) as month, 
                        count(reid)                   as reservation_count,
                        row_number() over 
                        (
                            partition by chid
                            order by count(reid) desc
                        ) as row_num
                    from chains
                        natural inner join hotel
                        natural inner join room
                        natural inner join roomunavailable
                        natural inner join reserve
                group by chid, name, month
                order by chid
            )
            select  chid,
                    name,
                    month, 
                    reservation_count as total_reservations
                from reservation_by_month
                where 
                    row_num <= 3
            order by chid, name, reservation_count desc
            """, ()
        )
        return result