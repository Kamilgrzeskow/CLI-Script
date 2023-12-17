import pymysql
from import_data import master

DATABASE_CREDENTIALS = {'host': 'localhost',
                        'user': 'root',
                        'password': 'my_data_base123',
                        'database': 'usersDB',
                        'charset': 'utf8',
                        'autocommit': True
                        }

COLUMNS_TO_CHECK_LOGIN = ["telephone_number", "email"]
TABLE_NAME = ["Users", "Children"]


def pass_credentials():
    return DATABASE_CREDENTIALS, TABLE_NAME


def table_create(c, database_name):
    create_table_user = f"""
    CREATE TABLE IF NOT EXISTS {database_name}.{TABLE_NAME[0]}(
        userID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        firstname VARCHAR(45) NOT NULL,
        telephone_number VARCHAR(45) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(45) NOT NULL,
        role VARCHAR(45) NOT NULL,
        created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    create_table_children = f"""
    CREATE TABLE IF NOT EXISTS {database_name}.{TABLE_NAME[1]}(
        childID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        parentID INT,
        childName VARCHAR(45),
        childAge INT,
        FOREIGN KEY (parentID) REFERENCES {TABLE_NAME[0]}(userID)
        );
"""

    c.execute(create_table_user)
    c.execute(create_table_children)


def insert_data_to_database(c):
    list_of_users = master()
    for user in list_of_users:
        c.execute(f"""
        INSERT INTO {TABLE_NAME[0]}(
        userID, firstname, telephone_number, email, password, role, created_at) 
        VALUES(NULL, %s, %s, %s, %s, %s, %s)
""", (
            user.firstname,
            user.telephone_number,
            user.email,
            user.password,
            user.role,
            user.created_at
        ))
        for child in user.list_of_children:
            c.execute(f"""
                    INSERT INTO {TABLE_NAME[1]}(
                    childID, parentID, childName, childAge) 
                    VALUES(NULL, %s, %s, %s)
            """, (
                int(list_of_users.index(user) + 1),
                child[0],
                child[1]
            ))


def print_all_accounts_db(login, password):
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {TABLE_NAME[0]}" \
                    f" WHERE (telephone_number='{login}' OR email='{login}') AND password='{password}'"
            cursor.execute(query)
            data = cursor.fetchall()
            exists = len(data) > 0
            if exists:
                for i in data:
                    if i[5] == "admin":
                        query_inside = f"SELECT * FROM {TABLE_NAME[0]}"
                        cursor.execute(query_inside)
                        data = cursor.fetchall()
                        print(len(data), end="")
                    else:
                        print("Invalid Login", end="")
            else:
                print("Invalid Login", end="")
    except pymysql.err.ProgrammingError as e:
        if "1054" in str(e):  # 1054 is the MySQL error code for "Unknown column"
            return False
        else:
            raise  # Re-raise other ProgrammingErrors
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def print_longest_existing_account_db(login, password):
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {TABLE_NAME[0]}" \
                    f" WHERE (telephone_number='{login}' OR email='{login}') AND password='{password}';"
            cursor.execute(query)
            data = cursor.fetchall()
            exists = len(data) > 0
            if exists:
                for i in data:
                    if i[5] == "admin":

                        query_inside = f"""
                            SELECT {TABLE_NAME[0]}.* 
                            FROM {TABLE_NAME[0]} 
                            JOIN (
                                SELECT MIN(created_at) AS earliest_TIMESTAMP
                                FROM {TABLE_NAME[0]}
                            ) AS subquery ON {TABLE_NAME[0]}.created_at = subquery.earliest_TIMESTAMP;
"""
                        cursor.execute(query_inside)
                        data = cursor.fetchall()
                        for j in data:
                            print(f"name: {j[1]}")
                            print(f"email: {j[3]}")
                            print(f"created_at: {j[6]}", end="")
                    else:
                        print("Invalid Login", end="")
            else:
                print("Invalid Login", end="")
    except pymysql.err.ProgrammingError as e:
        if "1054" in str(e):  # 1054 is the MySQL error code for "Unknown column"
            return False
        else:
            raise  # Re-raise other ProgrammingErrors
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def group_children_by_age_db(login, password):
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {TABLE_NAME[0]}" \
                    f" WHERE (telephone_number='{login}' OR email='{login}') AND password='{password}';"
            cursor.execute(query)
            data = cursor.fetchall()
            exists = len(data) > 0
            if exists:
                for i in data:
                    if i[5] == "admin":
                        children_dict = {}
                        query_inside = f"SELECT * FROM {TABLE_NAME[1]}"
                        cursor.execute(query_inside)
                        data = cursor.fetchall()
                        for j in data:
                            children_dict[j[3]] = 0
                        for j in data:
                            children_dict[j[3]] += 1
                        sorted_children_list = sorted(children_dict.items(), key=lambda x: x[1], reverse=False)
                        for j in range(len(sorted_children_list)):
                            if j != len(sorted_children_list) - 1:
                                print(f"age: {sorted_children_list[j][0]}, count: {sorted_children_list[j][1]}")
                            else:
                                print(f"age: {sorted_children_list[j][0]}, count: {sorted_children_list[j][1]}", end="")
                    else:
                        print("Invalid Login", end="")
            else:
                print("Invalid Login", end="")
    except pymysql.err.ProgrammingError as e:
        if "1054" in str(e):  # 1054 is the MySQL error code for "Unknown column"
            return False
        else:
            raise  # Re-raise other ProgrammingErrors
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def print_children_db(login, password):
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {TABLE_NAME[0]}" \
                    f" WHERE (telephone_number='{login}' OR email='{login}') AND password='{password}';"
            cursor.execute(query)
            data = cursor.fetchall()
            exists = len(data) > 0
            if exists:
                for user in data:
                    query_inside = f"""
                        SELECT *
                        FROM {TABLE_NAME[1]}
                        INNER JOIN {TABLE_NAME[0]} ON {TABLE_NAME[1]}.parentID = {TABLE_NAME[0]}.userID
                        WHERE parentID='{user[0]}';
"""
                    cursor.execute(query_inside)
                    data = cursor.fetchall()
                    sorted_children_list = sorted(data, key=lambda x: x[2], reverse=False)
                    for i in range(len(data)):
                        if i != len(data) - 1:
                            print(f"{sorted_children_list[i][2]}, {sorted_children_list[i][3]}")
                        else:
                            print(f"{sorted_children_list[i][2]}, {sorted_children_list[i][3]}", end="")
            else:
                print("Invalid Login", end="")
    except pymysql.err.ProgrammingError as e:
        if "1054" in str(e):  # 1054 is the MySQL error code for "Unknown column"
            return False
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def find_similar_children_by_age_db(login, password):
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {TABLE_NAME[0]}" \
                    f" WHERE (telephone_number='{login}' OR email='{login}') AND password='{password}';"
            cursor.execute(query)
            data = cursor.fetchall()
            exists = len(data) > 0
            if exists:
                for user in data:
                    query_inside = f"""
                    SELECT CONCAT(p.firstname, ', ', p.telephone_number, ': ') AS parent_info, 
                    GROUP_CONCAT(CONCAT(c.childName, ', ', c.childAge) 
                    ORDER BY c.childName SEPARATOR '; ') AS children_info 
                    FROM {TABLE_NAME[0]} p JOIN {TABLE_NAME[1]} c ON p.userID = c.parentID WHERE p.userID IN 
                    (SELECT DISTINCT parentID FROM {TABLE_NAME[1]} WHERE childAge IN 
                    (SELECT childAge FROM {TABLE_NAME[1]} WHERE parentID = {user[0]})) 
                    AND p.userID != {user[0]} GROUP BY p.userID;
"""
                    cursor.execute(query_inside)
                    data = cursor.fetchall()
                    for i in data:
                        for j in range(len(i)):
                            if j == 0:
                                print(i[j], end="")
                            else:
                                print(i[j])
            else:
                print("Invalid Login", end="")
    except pymysql.err.ProgrammingError as e:
        if "1054" in str(e):  # 1054 is the MySQL error code for "Unknown column"
            return False
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def config_main():
    conn = pymysql.connect(**DATABASE_CREDENTIALS)
    cursor = conn.cursor()
    table_create(cursor, DATABASE_CREDENTIALS['database'])
    insert_data_to_database(cursor)
    conn.close()


if __name__ == "__main__":
    config_main()
