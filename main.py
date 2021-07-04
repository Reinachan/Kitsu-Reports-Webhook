from dotenv import load_dotenv
from lib.report import fetch_reports
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

        cur = conn.cursor()
        return cur.execute("SELECT * from report")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    load_dotenv()

    cursor = create_connection(r"reports.db")

    fetch_reports(cursor)
