from model.db import Database


class global_stat_dao:


    def __init__(self):
        self.db = Database()


    def getMostCapacity(self):
        cur = self.db.connection.cursor()
        query = ("""select hname, sum(capacity) as total_capacity 
                    from hotel natural inner join room natural inner join roomdescription 
                    group by hid, hname 
                    order by total_capacity desc 
                    limit 5;""")
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result

    def getMostProfitMonth(self):
        cur = self.db.connection.cursor()
        query = ("""with extract_month_and_year as
                        (select chid as chainID, cname as name, extract(YEAR from startdate) as year, extract(MONTH from startdate) as month
                        from chains natural inner join hotel natural inner join room natural inner join roomunavailable),

                        total_reservations_by_month_year as
                            (select *, count(month) as total_reservations
                            from extract_month_and_year group by chainID,month,year,name order by chainID, total_reservations desc)

                    select name, year, month, total_reservations 
                    from (select *, row_number() over (partition by chainID order by total_reservations desc)
                    as highest from total_reservations_by_month_year) result
                    where highest <= 3;""")
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result