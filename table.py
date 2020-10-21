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
    """
    creates table to store past hw info
    """
    with sqlite3.connect("employee.db") as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS HW(
                       HW_ID          INTEGER PRIMARY KEY,
                       TITLE          TEXT,
                       CLASS          TEXT,
                       SUBJECT        TEXT,
                       DUE_DAY        INT,
                       DUE_MONTH      INT,
                       DUE_YEAR       INT,
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
                       CIRCULAR_DAY   INT,
                       CIRCULAR_MONTH INT,
                       CIRCULAR_YEAR  INT,
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
                       FROM_DAY       INT,
                       FROM_MONTH     INT,
                       FROM_YEAR      INT,
                       TO_DAY         INT,
                       TO_MONTH       INT,
                       TO_YEAR        INT,
                       DESCRIPTION    TEXT)"""
            )