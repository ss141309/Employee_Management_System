def tables():
    with sqlite3.connect("employee.db") as conn:
        conn.execute(''' CREATE TABLE IF NOT EXISTS empl(
                        FIRST_NAME VARCHAR(20),
                        LAST_NAME VARCHAR(10),
                        PASSWORD CHAR(64),
                        SALT VARCHAR(32))'''
                        )
