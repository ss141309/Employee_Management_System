import sqlite3


def tables():
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS EMPL(
                        EMP_ID     CHAR(6) PRIMARY KEY,
                        FIRST_NAME VARCHAR(20),
                        LAST_NAME  VARCHAR(10),
                        PASSWORD   BLOB,
                        SALT       BLOB)"""
        )
