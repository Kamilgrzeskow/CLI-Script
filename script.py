import argparse
from import_data import master
from datetime import datetime
from connection_check import check_database_connection
from users_database import (config_main,
                            print_all_accounts_db,
                            print_longest_existing_account_db,
                            group_children_by_age_db,
                            print_children_db,
                            find_similar_children_by_age_db)


list_of_users = master()  # Import list of users from import_data.py file


def check_database():
    check_first_table, check_second_table = check_database_connection()
    if check_first_table and check_second_table:
        return True
    else:
        return False


def create_database():
    config_main()


def print_all_accounts(login, password):  # Function shows the number of existing accounts
    if not check_database():
        try:
            flag = 0
            for user in list_of_users:
                if (user.telephone_number == login or user.email == login) and user.password == password:
                    flag = 1
                    if user.role == "admin":
                        print(int(len(list_of_users)), end="")
                    else:
                        print("Invalid Login", end="")
            if flag == 0:
                raise ValueError("Invalid user")

        except TypeError as e:
            print(f"Data provided has wrong format: {e}", end="")
        except ValueError:
            print(f"Invalid Login", end="")
        except Exception as e:
            print(f"There is an error: {e}", end="")
    else:
        print_all_accounts_db(login, password)


def print_longest_existing_account(login, password):  # Function shows the oldest account existing
    if not check_database():
        f = "%Y-%m-%d %H:%M:%S"
        list_of_dates = []
        flag = 0
        try:
            for user in list_of_users:
                if (user.telephone_number == login or user.email == login) and user.password == password:
                    flag = 1
                    if user.role == "admin":
                        for i in list_of_users:
                            s = i.created_at
                            out = datetime.strptime(s, f)
                            list_of_dates.append(out)
                        ind = list_of_dates.index(min(list_of_dates))
                        print(f"name: {list_of_users[ind].firstname}")
                        print(f"email: {list_of_users[ind].email}")
                        print(f"created_at: {list_of_users[ind].created_at}", end="")
                    else:
                        print("Invalid Login", end="")
            if flag == 0:
                raise ValueError("Wrong Login")
        except TypeError as e:
            print(f"Data provided has wrong format: {e}", end="")
        except ValueError:
            print(f"Invalid Login", end="")
        except Exception as e:
            print(f"There is an error: {e}", end="")
    else:
        print_longest_existing_account_db(login, password)


def group_children_by_age(login, password):  # Function shows grouped-by-age children
    if not check_database():
        children_dict = {}
        try:
            flag = 0
            for user in list_of_users:
                if (user.telephone_number == login or user.email == login) and user.password == password:
                    flag = 1
                    if user.role == "admin":
                        for i in list_of_users:
                            if len(i.list_of_children) > 0:
                                for j in range(len(i.list_of_children)):
                                    children_dict[i.list_of_children[j][1]] = 0
                        for i in list_of_users:
                            if len(i.list_of_children) > 0:
                                for j in range(len(i.list_of_children)):
                                    children_dict[i.list_of_children[j][1]] += 1
                        sorted_children_list = sorted(children_dict.items(), key=lambda x: x[1], reverse=False)
                        for i in range(len(sorted_children_list)):
                            if i != len(sorted_children_list) - 1:
                                print(f"age: {sorted_children_list[i][0]}, count: {sorted_children_list[i][1]}")
                            else:
                                print(f"age: {sorted_children_list[i][0]}, count: {sorted_children_list[i][1]}", end="")
                    else:
                        print("Invalid Login", end="")
            if flag == 0:
                raise ValueError("Wrong Login or/and Password")
        except TypeError as e:
            print(f"Data provided has wrong format: {e}", end="")
        except ValueError:
            print("Invalid Login", end="")
        except Exception as e:
            print(f"There is an error: {e}")
    else:
        group_children_by_age_db(login, password)


def print_children(login, password):  # Function shows children of user
    if not check_database():
        try:
            flag = 0
            for user in list_of_users:
                if (user.telephone_number == login or user.email == login) and user.password == password:
                    flag = 1
                    sorted_children_list = sorted(user.list_of_children, key=lambda x: x[0], reverse=False)
                    for i in range(len(user.list_of_children)):
                        if i != len(user.list_of_children) - 1:
                            print(f"{sorted_children_list[i][0]}, {sorted_children_list[i][1]}")
                        else:
                            print(f"{sorted_children_list[i][0]}, {sorted_children_list[i][1]}", end="")
            if flag == 0:
                raise ValueError("Wrong Login")
        except TypeError as e:
            print(f"Data provided has wrong format: {e}", end="")
        except ValueError:
            print("Invalid Login", end="")
        except Exception as e:
            print(f"There is an error: {e}", end="")
    else:
        print_children_db(login, password)


def find_similar_children_by_age(login, password):  # Function shows parents of children with similar age as user's
    if not check_database():
        temp_list_of_users = []
        try:
            flag = 0
            for user in list_of_users:
                if (user.telephone_number == login or user.email == login) and user.password == password:
                    flag = 1
                    for i in list_of_users:
                        temp_list_of_users.append(i)
                    temp_list_of_users.remove(user)
                    for i in temp_list_of_users:
                        for others_child in i.list_of_children:
                            for loggers_child in user.list_of_children:
                                if int(others_child[1]) == int(loggers_child[1]):
                                    print(f"{i.firstname}, {i.telephone_number}: ", end="")
                                    for j in range(len(i.list_of_children)):
                                        if j > 0:
                                            print("; ", end="")
                                        print(f"{i.list_of_children[j][0]}, {i.list_of_children[j][1]}", end="")
                                    print("")
                                break
            if flag == 0:
                raise ValueError
        except TypeError as e:
            print(f"Data provided has wrong format: {e}", end="")
        except ValueError:
            print("Invalid Login", end="")
        except Exception as e:
            print(f"There is an error: {e}", end="")
    else:
        find_similar_children_by_age_db(login, password)


def main():  # Initiate argument parsing
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("command",
                            choices=["print-all-accounts",
                                     "print-oldest-account",
                                     "group-by-age",
                                     "print-children",
                                     "find-similar-children-by-age",
                                     "create_database"],
                            help="The command to execute")
        parser.add_argument("--login", required=False, help="Login information")
        parser.add_argument("--password", required=False, help="Password information")

        args = parser.parse_args()

        # React based on the provided command
        if args.command == "print-all-accounts":
            print_all_accounts(args.login, args.password)
        elif args.command == "print-oldest-account":
            print_longest_existing_account(args.login, args.password)
        elif args.command == "group-by-age":
            group_children_by_age(args.login, args.password)
        elif args.command == "print-children":
            print_children(args.login, args.password)
        elif args.command == "find-similar-children-by-age":
            find_similar_children_by_age(args.login, args.password)
        elif args.command == "create_database":
            create_database()
        else:
            print("Invalid command")
    except Exception as e:
        print(f"An error occurred: {e}")
    return args.login, args.password


if __name__ == "__main__":
    main()
