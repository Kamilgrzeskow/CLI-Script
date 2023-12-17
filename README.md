It is a CLI Script which imports and merges the data from XML, CSV and JSON.
The data contains information about users and their children.
To use it simply open terminal at CLI Script directory and type:
    python script.py <command> --login <login> --password <password>
The commands are within quotes:
    "create_database" - creates a database tables and inserts the data: changes the way that other commands work
    "print-all-accounts" - prints number of all accounts - requires admin account to login
    "print-oldest-account" - prints the information about the earliest created account - requires admin account to login
    "group-by-age" - prints numbers of children of certain ages - requires admin account to login
    "print-children" - prints children of logged user
    "find-similar-children-by-age" - prints the information about parents who have children in the same age 
as logged user and their children - works a bit differently with create_database command because I didn't have time
to manage the SQL query that acts the same way. But I think it matches the task: "Find users with children of the same
age as at least one own child, print the user and all of his children data".
 
To add new data, put the line in the "import_data.py"'s master() function just between the last 
    "list_of_users = import_file(<directory_to_file>, list_of_users)" and 
    "list_of_users = merge_data(list_of_users)":
    "list_of_users = import_file(<directory_to_your_file>, list_of_users)"

When executing the script with the file attached in the project the example input could be (I recommend to put the
password in the quotes "" so the argparser could not make a mistake): 
    python script.py <command> --login ngreen@example.org --password "n(9vNQ$jqO"
There is a test_script.py file you can use typing:
    python test_script.py
If the data is provided as in repository: test should go OK but one test is going to fail when "create_database"
command is done.
Project is owned by Kamil Grześków
