import sqlite3
import bcrypt


def insert_application(first_name, last_name, email, start_date, occupation):
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


def insert_account(account_name, plaintext_password, list_roles):
    try:
        encryption_salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(plaintext_password.encode("UTF-8"), encryption_salt)
        connection = sqlite3.Connection("./instance/data.db")
        cursor = connection.cursor()
        insert_statement = "INSERT INTO ACCOUNT (username, password, isActive) VALUES (?, ?, true)"
        cursor.execute(insert_statement, (account_name, encrypted_password))
        cursor.connection.commit()

        account = select_account_by_account_name(account_name)
        print(account)
        for str_role in list_roles:
            role = select_role_by_role_name(str_role)
            insert_account_role(account[0], role[0])
        print(cursor.rowcount)
        return cursor.rowcount
    except Exception as error:
        print(error)
        return 0


def select_account_by_account_name(account_name):
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT * FROM ACCOUNT WHERE username = ?"
    result = connection.execute(select_statement, (account_name,)).fetchone()
    return result


def select_role_by_role_name(role_name):
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT * FROM ROLE WHERE role_name = ?"
    result = connection.execute(select_statement, (role_name,)).fetchone()
    return result


def insert_account_role(account_id, role_id):
    connection = sqlite3.Connection("./instance/data.db")
    cursor = connection.cursor()
    insert_statement = "INSERT INTO ACCOUNT_ROLE (account_id, role_id) VALUES (?, ?)"
    cursor.execute(insert_statement, (account_id, role_id))
    cursor.connection.commit()
    return cursor.rowcount
