"""
Create a db_operations.py module with a DBOperations class inside
By: Ha Phuong Le & Nguyen Anh Thu Mai
"""
import logging
from dbcm import DBCM

class DBOperations():
    """
    Use the Python sqlite3 module to store the weather data in SQLite db and retrieve data
    By: Ha Phuong Le & Nguyen Anh Thu Mai
    """
    def __init__(self, database):
        """
        Initialize the attributes
        By: Nguyen Anh Thu Mai
        """
        try:
            self.database = database
        except Exception as exception:
            logging.error(f"WeatherScraper:__init__:{exception}")

    def fetch_data(self, date):
        """
        Fetch data from the database as requested by the user input
        By: Ha Phuong Le
        """
        try:
            with DBCM(self.database) as cur:
                for row in cur.execute("select avg_temp from samples where sample_date=?", (date,)):
                    try:
                        return row[0]
                    except Exception as exception:
                        logging.error(f"DBOperations:fetch_data:loop:{exception}")
        except Exception as exception:
            logging.error(f"DBOperations:fetch_data:{exception}")

    def save_data(self, mydict):
        """
        Store data into the existed db
        By: Ha Phuong Le
        """
        try:
            sql = """insert into samples (sample_date, location, max_temp, min_temp, avg_temp)
            values (?,?,?,?,?)"""
            for day, temps in mydict.items():
                try:
                    avg_temp = self.fetch_data(day)

                    if avg_temp is None:
                        data = (day, 'Winnipeg, MB', temps['Max'], temps['Min'], temps['Mean'])

                        with DBCM(self.database) as cur:
                            cur.execute(sql, data)
                except Exception as exception:
                    logging.error(f"DBOperations:save_data:loop:{exception}")
        except Exception as exception:
            logging.error(f"DBOperations:save_data:{exception}")

    def initialize_db(self):
        """
        Initialize the db
        By: Nguyen Anh Thu Mai
        """
        try:
            with DBCM(self.database) as cur:
                cur.execute("""create table if not exists samples
                            (id integer primary key autoincrement not null,
                            sample_date text not null,
                            location text not null,
                            max_temp real not null,
                            min_temp real not null,
                            avg_temp real not null);""")
        except Exception as exception:
            logging.error(f"DBOperations:initialize_db:{exception}")

    def purge_data(self):
        """
        Purge the table in db if exists
        By: Nguyen Anh Thu Mai
        """
        try:
            with DBCM(self.database) as cur:
                cur.execute("drop table if exists samples")
        except Exception as exception:
            logging.error(f"DBOperations:purge_data:{exception}")

    def get_latest_date(self):
        """
        Return the latest date of data in db
        By: Ha Phuong Le
        """
        try:
            with DBCM(self.database) as cur:
                for row in cur.execute("select max(sample_date) from samples"):
                    try:
                        return row[0]
                    except Exception as exception:
                        logging.error(f"DBOperations:get_latest_date:loop:{exception}")
        except Exception as exception:
            logging.error(f"DBOperations:get_latest_date:{exception}")
