import sqlite3
import bcrypt


def insert_application(first_name, last_name, email, start_date, occupation):
    connection = sqlite3.Connection("./instance/data.db")
    cursor = connection.cursor()
    insert_statement = f"INSERT INTO APPLICATION (first_name, last_name, email, start_date, occupation, accepted) " \
                       f"VALUES (?, ?, ?, ?, ?, false)"
    cursor.execute(insert_statement, [first_name, last_name, email, start_date, occupation])
    cursor.connection.commit()
    print(cursor.rowcount)
    return cursor.rowcount


def select_applications():
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT * FROM APPLICATION"
    result = connection.execute(select_statement).fetchall()
    return result


def accept_application(application_id):
    connection = sqlite3.Connection("./instance/data.db")
    update_statement = "UPDATE APPLICATION SET accepted = 1 WHERE id = ?"
    result = connection.execute(update_statement, (application_id,))
    connection.commit()
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


def read_role_id_by_account_id(account_id):
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT * FROM ACCOUNT_ROLE where account_id = ?"
    result = connection.execute(select_statement, (account_id,)).fetchall()
    return result


def read_role_name_by_role_id(role_id):
    connection = sqlite3.Connection("./instance/data.db")
    select_statement = "SELECT role_name FROM ROLE where role_id = ?"
    result = connection.execute(select_statement, (role_id,)).fetchone()
    print(result)
    return result[0]
