import sqlite3


def tables() -> None:
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS EMPL(
                        EMP_ID     TEXT PRIMARY KEY,
                        FIRST_NAME TEXT,
                        LAST_NAME  TEXT,
                        PASSWORD   BLOB,
                        SALT       BLOB)"""
        )


def hw_table() -> None:
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS HW(
                       HW_ID INTEGER PRIMARY KEY,
                       TITLE TEXT,
                       CLASS TEXT,
                       SUBJECT TEXT,
                       DESCRIPTION TEXT)"""
        )
