import mysql.connector

from .config import config


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establishes a new database connection.
        """
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
            )
            self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        """
        Closes the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_cursor(self):
        """
        Returns the database cursor.
        """
        return self.cursor

    def commit(self):
        """
        Commits the current transaction.
        """
        if self.connection:
            self.connection.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        self.close()
