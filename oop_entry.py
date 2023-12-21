from glob import glob
import xmltodict
import csv
import json
from datetime import datetime

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class DataReader:

    @staticmethod
    def read_xml(file_path):
        with open(file_path, 'r') as file:
            data = xmltodict.parse(file.read())
        data = data['users']['user']
        for user in data:
            children_list = []
            if user['children'] is not None:
                if isinstance(user['children']['child'], dict):
                    children_list.append(user['children']['child'])
                else:
                    for child in user['children']['child']:
                        children_list.append(child)
            user['children'] = children_list
        return data

    @staticmethod
    def read_csv(file_path):
        data = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                children = row['children'].split(',')
                children_list = []
                if children != ['']:
                    for child in children:
                        child_attrib = child.split(' ')
                        child_dict = {'name': child_attrib[0], 'age': child_attrib[1].strip('()')}
                        children_list.append(child_dict)
                row['children'] = children_list
                data.append(row)
        return data

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


class User:  # Creating a class and constructor for our users

    def __init__(self, firstname, telephone_number, email,
                 password, role, created_at, children=None):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.children = children or []

    def __repr__(self):
        return (f"Firstname: {self.firstname}, telephone_number: {self.telephone_number}, "
                f"email: {self.email}, password: {self.password}, role: {self.role}, "
                f"created_at: {self.created_at}")

    def __hash__(self):
        # tiffany sie powtarza 65 i 66 rekord zrobić że jeden hasz to albo te
        return hash((self.firstname, self.telephone_number, self.email, self.password, self.role, tuple(self.children)))

    def __eq__(self, other):
        # return (isinstance(other, User) and
        #         self.firstname == other.firstname and
        #         self.telephone_number == other.telephone_number and
        #         self.email == other.telephone_number and
        #         self.password == other.password and
        #         self.role == other.role and
        #         self.children == other.children)
        return (
                (isinstance(other, User) and
                 self.firstname == other.firstname and
                 self.telephone_number == other.telephone_number and
                 self.password == other.password and
                 self.role == other.role and
                 self.children == other.children) or
                (isinstance(other, User) and
                 self.firstname == other.firstname and
                 self.email == other.email and
                 self.password == other.password and
                 self.role == other.role and
                 self.children == other.children))


class Child:
    def __init__(self, name, age, parent):
        self.name = name
        self.age = age
        self.parent = parent

    def __repr__(self):
        return f"Name: {self.name}, age: {self.age}"


class DataValidation:
    users_to_delete = []

    def __init__(self, users):
        self.users = users

    @classmethod
    def validate_email(cls, user):
        split_email_at = user.email.split("@")
        split_email_dot = user.email.split(".")
        if (user.email.count("@") > 1 or
                len(split_email_at[0]) < 1 or
                split_email_at[1].find(".") < 1 or
                not split_email_dot[-1].isalnum() or
                not 0 < len(split_email_dot[-1]) < 5):
            cls.users_to_delete.append(user)

    @staticmethod
    def telephone_validation(number):
        number = ''.join(char for char in number if char.isdigit())
        if len(number) > 9:
            number = number[-9:]
        return number

    def data_validation(self):
        for user in self.users:
            self.validate_email(user)
            user.telephone_number = self.telephone_validation(user.telephone_number)
        for user_ in self.users_to_delete:
            print(f"usuwam {user_}")
            self.users.remove(user_)


class DataManager:
    users = []

    def __init__(self):
        self.data = []

    def import_data(self):
        for file_path in glob('InputData/**/*.xml', recursive=True):
            self.data.extend(DataReader.read_xml(file_path))
        for file_path in glob('InputData/**/*.csv', recursive=True):
            self.data.extend(DataReader.read_csv(file_path))
        for file_path in glob('InputData/**/*.json', recursive=True):
            self.data.extend(DataReader.read_json(file_path))

    def add_user_removing_duplicates(self, user):
        if user not in self.users:
            self.users.append(user)
        else:
            for dplct in self.users:
                if dplct == user and user.created_at > dplct.created_at:
                    print(f"Ten co rzekomo nowszy: {user}, i ten co starszy: {dplct}")
                    self.users.remove(dplct)
                    self.users.append(user)

    def create_user_from_data(self, data):
        for entry in self.data:
            created_at = datetime.strptime(entry['created_at'], DATE_TIME_FORMAT)
            user = User(
                firstname=entry['firstname'],
                telephone_number=entry['telephone_number'],
                email=entry['email'],
                password=entry['password'],
                role=entry['role'],
                created_at=created_at,
                children=[]
            )
            children_data = entry.get('children')
            children_instances = [Child(child['name'], child['age'], user) for child in children_data]
            user.children = children_instances
            self.add_user_removing_duplicates(user)

    @classmethod
    def user_display(cls):
        for i, v in enumerate(cls.users):
            print(i + 1, v)
        print(len(cls.users))


if __name__ == '__main__':
    data_manager = DataManager()
    data_manager.import_data()
    data_manager.create_user_from_data(data_manager.data)
    data_validator = DataValidation(data_manager.users)
    data_validator.data_validation()

    data_manager.user_display()
