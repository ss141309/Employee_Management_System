import sqlite3


def tables() -> None:
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS EMPL(
                        EMP_ID                TEXT PRIMARY KEY,
                        FIRST_NAME            TEXT,
                        LAST_NAME             TEXT,
                        PASSWORD              BLOB,
                        SALT                  BLOB,
                        CONTACT               TEXT,
                        EMAIL                 TEXT,
                        DOB_DAY               INT,
                        DOB_MONTH             TEXT,
                        DOB_YEAR              INT,
                        JOINING_DAY           INT,
                        JOINING_MONTH         TEXT,
                        JOINING_YEAR          INT,
                        CLASSES_ASSIGNED      TEXT,
                        SUBJECTS              TEXT,
                        BUS_ROUTE             TEXT,
                        ADDRESS               TEXT
                        )"""
        )


def hw_table() -> None:
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS HW(
                       HW_ID INTEGER PRIMARY KEY,
                       TITLE TEXT,
                       CLASS TEXT,
                       SUBJECT TEXT,
                       DUE_DAY INT,
                       DUE_MONTH INT,
                       DUE_YEAR INT,
                       DESCRIPTION TEXT)"""
        )