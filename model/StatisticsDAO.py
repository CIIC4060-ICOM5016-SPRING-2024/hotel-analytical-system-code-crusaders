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
            select  rdid, rname, rtype,
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
                    hid = 1
            group by rid
            order by datediff asc
            limit 3;
            """,
            (id,)
        )
        return result

    def get_MostCreditCard(self, id):
        """
        select fname, lname, count (*) as count_reservation 
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
        """

    def get_HighestPaid(self, id):
        """
        select  eid,
                fname || ' ' || lname as full_name,
                salary 
            from employee
            where
                hid = 1 and
                position = 'Regular' 
        order by salary desc
        limit 3;
        """
        pass

    def get_MostDiscount(self, id):
        result = Database().querySelectFrom(
            """
            select  clid,
                    fname || ' ' || lname        as full_name,
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
        """
        pass
    
    def get_LeastGuests(self, id):
        """"
        select rid,cast(cast((guests) as decimal) / (capacity) as decimal(20,3)) as ratio from
        (select rid, guests, capacity
        from roomdescription natural inner join room natural inner join roomunavailable natural inner join reserve
            where hid = 1
        group by rid,guests,capacity
        order by rid)
        order by ratio asc
        limit 3;


        select  rid,
                cast(cast((guests) as decimal) / (capacity) as decimal(20,3)) as ratio
            from room
                natural inner join roomdescription
                natural inner join roomunavailable
                natural inner join reserve
            where
                hid = 1
        group by rid, guests, capacity
        order by ratio asc
        limit 3;
        """
        pass

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