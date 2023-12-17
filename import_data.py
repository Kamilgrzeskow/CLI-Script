from datetime import datetime
import xml.etree.ElementTree as ET
import json
import csv


class Users:  # Creating a class and constructor for our users

    def __init__(self, firstname, telephone_number, email,
                 password, role, created_at):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.list_of_children = []

    def __str__(self):
        return f"User = {self.firstname}"


def email_validation(email):
    if email.count("@") > 1:
        return False
    split_email_at = email.split("@")
    if len(split_email_at[0]) < 1:
        return False
    if split_email_at[1].find(".") < 1:
        return False
    split_email_dot = email.split(".")
    if split_email_dot[-1].isalnum():
        if 0 < len(split_email_dot[-1]) < 5:
            return True
        return False


def telephone_number_parsing(number_in):
    number = ''.join(char for char in number_in if char.isdigit())
    if len(number) > 9:
        number = number[-9:]
    return number


def import_file(directory_to_file, initial_list_of_users):  # Choosing file type to proceed
    try:
        if directory_to_file.endswith(".xml"):
            tree = ET.parse(directory_to_file)
            users = tree.getroot()
            list_of_users = make_data_from_xml(users, initial_list_of_users)
            return list_of_users
        elif directory_to_file.endswith(".json"):
            with open(directory_to_file, "r") as json_file:
                users = json.load(json_file)
                list_of_users = make_data_from_json(users, initial_list_of_users)
                return list_of_users
        elif directory_to_file.endswith(".csv"):
            with open(directory_to_file, "r") as csv_file:
                users = csv.reader(csv_file)
                list_of_users = make_data_from_csv(users, initial_list_of_users)
                return list_of_users
        else:
            raise TypeError("There is no file that can be read")
    except TypeError as TE:
        print(f"Error: {TE}")


def make_data_from_xml(data_not_loaded, data_loaded):  # XML parser function
    users = data_not_loaded
    list_of_users = data_loaded
    temp_list_of_users = []
    for i in range(len(users)):
        firstname = users[i][0].text.strip()
        if users[i][1].text is not None:
            telephone_number = telephone_number_parsing(users[i][1].text.strip())
            if telephone_number == "":
                continue
        elif users[i][1].text is None:
            continue
        email = users[i][2].text.strip()
        e_validation = email_validation(email)
        if not e_validation:
            continue
        password = (str(ET.tostring(users[i][3]))
                    .lstrip("b")
                    .replace("<password>", "")
                    .replace("</password>", "")
                    .strip("'")
                    )
        role = users[i][4].text.strip()
        created_at = users[i][5].text.strip()
        user_instance = Users(firstname,
                              telephone_number,
                              email,
                              password,
                              role,
                              created_at)
        temp_list_of_users.append(user_instance)
    for i in range(len(users)):
        for child in users[i][6]:
            child_tuple = child[0].text.strip(), int(child[1].text.strip())
            temp_list_of_users[i].list_of_children.append(child_tuple)
    list_of_users.extend(temp_list_of_users)
    return list_of_users


def make_data_from_json(data_not_loaded, data_loaded):  # JSON parser function
    users = data_not_loaded
    list_of_users = data_loaded
    temp_list_of_users = []
    for user in range(len(users)):
        users_dict = users[user]
        firstname = users_dict['firstname']
        telephone_number = users_dict['telephone_number']
        telephone_number = telephone_number_parsing(telephone_number)
        if telephone_number == "":
            continue
        email = users_dict['email']
        e_validation = email_validation(email)
        if not e_validation:
            continue
        password = users_dict['password']
        role = users_dict['role']
        created_at = users_dict['created_at']
        user_instance = Users(firstname, telephone_number, email, password, role, created_at)
        temp_list_of_users.append(user_instance)
        for child in users_dict['children']:
            child_tuple = (child['name'], int(child['age']))
            temp_list_of_users[user].list_of_children.append(child_tuple)
    list_of_users.extend(temp_list_of_users)
    return list_of_users


def make_data_from_csv(data_not_loaded, data_loaded):  # CSV parser function
    users = data_not_loaded
    list_of_users = data_loaded
    temp_list_of_users = []
    count = -1
    for user in users:
        user_list = []
        count += 1
        for i in range(len(user)):
            if i == 0:
                user_list = user[i].split(";")
            elif i > 0:
                user_list.append(user[i])
        if user_list[0] == 'firstname':
            count -= 1
            continue
        firstname = user_list[0]
        telephone_number = user_list[1]
        telephone_number = telephone_number_parsing(telephone_number)
        if telephone_number == "":
            count -= 1
            continue
        email = user_list[2]
        e_validation = email_validation(email)
        if not e_validation:
            count -= 1
            continue
        password = user_list[3]
        role = user_list[4]
        created_at = user_list[5]
        user_instance = Users(firstname, telephone_number, email, password, role, created_at)
        temp_list_of_users.append(user_instance)
        if user_list[6] != "":
            for i in range(6, len(user_list)):
                child_tuple = user_list[i].split(" ")[0], int(user_list[i].split(" ")[1].strip("()"))
                temp_list_of_users[count].list_of_children.append(child_tuple)
    list_of_users.extend(temp_list_of_users)

    return list_of_users


def merge_data(data_in):  # Remove duplicates function
    time_format = "%Y-%m-%d %H:%M:%S"
    list_of_dates = []
    try:
        if type(data_in) == "NoneType":
            raise TypeError("Type Error")
        list_of_users = data_in
        users_to_delete = []
        for user in list_of_users:
            string = user.created_at
            output_date = datetime.strptime(string, time_format)
            list_of_dates.append(output_date)
        for i in range(len(list_of_users)):
            for j in range(i + 1, len(list_of_users)):
                if (
                    list_of_users[i].email == list_of_users[j].email
                    or list_of_users[i].telephone_number == list_of_users[j].telephone_number
                ):
                    if list_of_dates[i] > list_of_dates[j]:
                        users_to_delete.append(list_of_users[j])
                    elif list_of_dates[i] < list_of_dates[j]:
                        users_to_delete.append(list_of_users[i])
                    elif list_of_dates[i] == list_of_dates[j]:
                        users_to_delete.append(list_of_users[i])
        for user in users_to_delete:
            list_of_users.remove(user)
    except TypeError as e:
        print(f"This dataset contains unmatching data convention: {e}")
    return list_of_users


def master():  # Entry function
    list_of_users = []
    list_of_users = import_file("InputData/data/users_2.xml", list_of_users)
    list_of_users = import_file("InputData/data/a/b/users_1.xml", list_of_users)
    list_of_users = import_file("InputData/data/a/users.json", list_of_users)
    list_of_users = import_file("InputData/data/a/b/users_1.csv", list_of_users)
    list_of_users = import_file("InputData/data/a/c/users_2.csv", list_of_users)
    # list_of_users = import_file("users.txt", list_of_users)

    list_of_users = merge_data(list_of_users)
    return list_of_users


if __name__ == "__main__":
    master()
