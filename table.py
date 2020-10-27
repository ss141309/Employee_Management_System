import sqlite3


def tables() -> None:
    """
    creates table to store employee information
    """
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
                        DOB                   TEXT,
                        JOIN_DATE             TEXT,
                        CLASSES               TEXT,
                        SUBJECTS              TEXT,
                        BUS_ROUTE             TEXT,
                        ADDRESS               TEXT
                        )"""
        )


def hw_table() -> None:
    """
    creates table to store past hw info
    """
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS HW(
                       HW_ID          INTEGER PRIMARY KEY,
                       ASSIGNED_BY    TEXT,
                       TITLE          TEXT,
                       CLASS          TEXT,
                       SUBJECT        TEXT,
                       DUE_DATE       TEXT,
                       DESCRIPTION    TEXT)"""
        )


def circular_table() -> None:
    """
    creates table to store circulars
    """
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS CIRCULAR(
                       TITLE          TEXT,
                       CIRCULAR_DATE  TEXT,
                       DESCRIPTION    TEXT)"""
        )


def leave_table() -> None:
    """
    creates table to store leave info
    """
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS LEAVEINFO(
                       LI_ID          INTEGER PRIMARY KEY,
                       TH_ID          TEXT,
                       TITLE          TEXT,
                       FROM_DATE      TEXT,
                       TO_DATE        TEXT,
                       DESCRIPTION    TEXT)"""
        )


def student_table() -> None:
    """
    creates table to store student data
    """
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS STUDENT(
                      STUDENT_ID TEXT PRIMARY KEY,
                      FIRST_NAME TEXT,
                      LAST_NAME TEXT,
                      GENDER TEXT,
                      DOB    TEXT,
                      JOIN_DATE TEXT,
                      CLASS TEXT,
                      HOUSE TEXT,
                      ROLL_NO INT,
                      BUS_ROUTE TEXT,
                      EMAIL TEXT,
                      CONTACT TEXT,
                      ADDRESS TEXT) """
        )
