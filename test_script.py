import unittest
from unittest.mock import patch
from io import StringIO
from script import main


class TestScript(unittest.TestCase):

    @patch("sys.argv", ["script.py", "print-all-accounts", "--login", "817730653", "--password", "4^8(Oj52C+"])
    def test_print_all_accounts_admin(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "84")

    @patch("sys.argv", ["script.py", "print-oldest-account", "--login",
                        "woodsjerry@example.com", "--password", "z2Y%0Hbcsi"])
    def test_print_all_accounts_user(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Invalid Login")

    @patch("sys.argv", ["script.py", "print-oldest-account", "--login", "817730653", "--password", "4^8(Oj52C+"])
    def test_print_oldest_account_admin(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "name: Justin\nemail: opoole@example.org\n"
                                     "created_at: 2022-11-25 02:19:37")

    @patch("sys.argv", ["script.py", "print-oldest-account", "--login",
                        "litiffany@example.org", "--password", "!Y2m4%ysM4"])
    def test_print_oldest_account_user(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Invalid Login")

    @patch("sys.argv", ["script.py", "group-by-age",
                        "--login", "817730653", "--password", "4^8(Oj52C+"])
    def test_group_children_by_age_admin(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "age: 5, count: 4\nage: 10, count: 4\nage: 14, count: 4\nage: 18, count: 5\n"
                                     "age: 15, count: 5\nage: 7, count: 5\nage: 6, count: 5\nage: 9, count: 5\n"
                                     "age: 16, count: 5\nage: 3, count: 7\nage: 13, count: 7\nage: 4, count: 7\n"
                                     "age: 8, count: 9\nage: 12, count: 9\nage: 11, count: 10\nage: 17, count: 10\n"
                                     "age: 2, count: 10\nage: 1, count: 10")

    @patch("sys.argv", ["script.py", "group-by-age", "--login",
                        "alicia41@example.com", "--password", "^rf3mkTt&amp;)"])
    def test_group_children_by_age_user(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Invalid Login")

    @patch("sys.argv", ["script.py", "print-children", "--login",
                        "johnperry@example.com", "--password", "bd6GvDNA!+"])
    def test_print_children(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Bradley, 13\nRachel, 8")

    @patch("sys.argv", ["script.py", "find-similar-children-by-age",
                        "--login", "318506164", "--password", "bd6GvDNA!+"])
    def test_find_similar_children_by_age(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Amanda, 698312978: Christopher, 15; Lisa, 8; Brenda, 1\n"
                                     "Mark, 967426092: Tracy, 1; Joseph, 1; Whitney, 8\n"
                                     "Amy, 361568741: Sara, 8\nAmanda, 208579481: Marie, 17; George, 8; Susan, 11\n"
                                     "Sarah, 401629185: Michael, 8; Michelle, 9\n"
                                     "Chad, 882294581: Diana, 17; April, 8; James, 17\n"
                                     "Christopher, 743328816: Scott, 5; James, 9; Zachary, 8\n"
                                     "Curtis, 107058738: Eric, 8; Shelia, 17")

    @patch("sys.argv", ["script.py", "print-children", "--login", "123456798", "--password", "rewuydsfg"])
    def test_fake_user(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Invalid Login")


if __name__ == "__main__":
    unittest.main()
