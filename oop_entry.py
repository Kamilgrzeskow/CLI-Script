from glob import glob
import xmltodict
import csv
import json


class DataReader:

    @staticmethod
    def read_xml(file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            data = xmltodict.parse(file.read())
            data = data['users']['user']
        return data

    @staticmethod
    def read_csv(file_path):
        data = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data


class Users:  # Creating a class and constructor for our users

    def __init__(self, firstname, telephone_number, email,
                 password, role, created_at, children=None):
        self.firstname = firstname
        self.telephone_number = telephone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.children = children or []

    def validate_email(self):
        if self.email.count("@") > 1:
            return False
        split_email_at = self.email.split("@")
        if len(split_email_at[0]) < 1:
            return False
        if split_email_at[1].find(".") < 1:
            return False
        split_email_dot = self.email.split(".")
        if split_email_dot[-1].isalnum():
            if 0 < len(split_email_dot[-1]) < 5:
                return True
            return False


class Child:

    def __init__(self, name, age):
        self.name = name
        self.age = age


class DataManager:

    def __init__(self):
        self.users = []

    def import_data(self):
        for file_path in glob('InputData/**/*.xml', recursive=True):
            self.users.append(DataReader.read_xml(file_path))
        for file_path in glob('InputData/**/*.csv', recursive=True):
            self.users.append(DataReader.read_csv(file_path))
        for file_path in glob('InputData/**/*.json', recursive=True):
            self.users.append(DataReader.read_json(file_path))

    def remove_duplicates(self):
        pass


def main():
    data_manager = DataManager()
    print(data_manager.users)
    data_manager.import_data()
    for i in data_manager.users:
        print(i)


if __name__ == '__main__':
    main()
