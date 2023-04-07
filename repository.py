import os
import sqlite3


def insert_application(first_name, last_name, email, start_date, occupation):
    print(os.getcwd())
    connection = sqlite3.Connection("./instance/data.db")
    cursor = connection.cursor()
    insert_statement = f"INSERT INTO APPLICATION (first_name, last_name, email, start_date, occupation) VALUES " \
                       "(?, ?, ?, ?, ?)"
    cursor.execute(insert_statement, [first_name, last_name, email, start_date, occupation])
    cursor.connection.commit()
    print(cursor.rowcount)
    return cursor.rowcount


def select_applications():
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT * FROM APPLICATION"
    result = connection.execute(select_statement).fetchall()
    return result
