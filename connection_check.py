import pymysql
from users_database import pass_credentials


def check_database_connection():
    database_credentials, table_name = pass_credentials()
    conn = pymysql.connect(**database_credentials)
    cursor = conn.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name[0]}'")
    check_first_table = cursor.fetchone() is not None
    cursor.execute(f"SHOW TABLES LIKE '{table_name[1]}'")
    check_second_table = cursor.fetchone() is not None
    conn.close()
    return check_first_table, check_second_table
