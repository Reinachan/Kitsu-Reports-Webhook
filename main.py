from dotenv import load_dotenv
from lib.report import fetch_reports
import sqlite3
from sqlite3 import Error


import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def main():
    database = r"reports.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        fetch_reports(conn)


if __name__ == "__main__":
    load_dotenv()
    main()
