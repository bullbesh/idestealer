import sqlite3


def add_id(people_id, user_id):
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS login_id(
    	id INTEGER
    )"""
    )

    connect.commit()

    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
    else:
        pass

    cursor.close()
    connect.close()


def delete_id(people_id):
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()

    cursor.close()
    connect.close()
