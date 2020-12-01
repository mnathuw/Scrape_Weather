"""
Create a context manager called DBCM to manage the database connections.
By: Nguyen Anh Thu Mai
"""
import logging
import sqlite3

class DBCM:
    """
    Create a context manager for db connection and cursor
    By: Nguyen Anh Thu Mai
    """
    def __init__(self, database):
        """
        Initialize the database connection
        By: Nguyen Anh Thu Mai
        """
        try:
            self.data = database
            self.conn = None
            self.cur = None
        except Exception as exception:
            logging.error(f"DBCM:__init__: {exception}")

    def __enter__(self):
        """
        Make a db connection and return the cursor
        By: Nguyen Anh Thu Mai
        """
        try:
            self.conn = sqlite3.connect(self.data)
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as exception:
            logging.error(f"DBCM:__enter__: {exception}")

    def __exit__(self, *exc):
        """
        Close db connection
        By: Nguyen Anh Thu Mai
        """
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as exception:
            logging.error(f"DBCM:__exit__: {exception}")
