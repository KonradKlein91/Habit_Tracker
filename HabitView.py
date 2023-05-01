from Habit import Habit
from HabitController import HabitController
from tabulate import tabulate


class HabitView:
    """
    View class for the Habit application
    """

    def __init__(self):
        self.controller = HabitController()

    def run(self):
        """
        Runs the Habit application and creates a loop that shows the main menu and then calls the appropriate method
        :return: None
        """
        while True:
            self.show_main_menu()
            choice = input("please enter the number of the task you would like to execute: ")
            if choice == "1":
                self.add_habit()
            elif choice == "2":
                self.delete_habit()
            elif choice == "3":
                self.complete_habit()
            elif choice == "4":
                self.show_habits_table()
            elif choice == "5":
                self.show_longest_streak()
            elif choice == "6":
                self.show_longest_streak_habit()
            elif choice == "7":
                self.show_habits_frequency()
            elif choice == "8":
                self.show_habit_names()
            elif choice == "9":
                self.show_completed_within_last_week()
            elif choice == "10":
                self.insert_sample_data()
            elif choice == "11":
                self.clear_database()
            elif choice == "q":
                break
            else:
                print("Invalid choice. Please try again.")

    def show_main_menu(self):
        """
        prints the main menu
        :return: None
        """
        menu = [
            ["1.", "add a new habit"],
            ["2.", "delete a habit"],
            ["3.", "complete a habit"],
            ["4.", "show all habits"],
            ["5.", "show longest streaks"],
            ["6.", "show longest streak for a habit"],
            ["7.", "show habits with certain frequency"],
            ["8.", "show habit names"],
            ["9.", "show completed habits last week"],
            ["10.", "insert sample data"],
            ["11.", "clear database"],
            ["q.", "quit"]
        ]
        headers = ["Main Menu", "Task"]
        print(tabulate(menu, headers=headers, tablefmt="fancy_grid"))

    def add_habit(self):
        """
        gets the new habit info from the user and calls the controller to add the habit
        :return: None
        """
        Habit = self.get_new_habit_info_from_user()
        self.controller.add_habit(Habit)
        print_end()

    def delete_habit(self):
        """
        calls the controller to delete the habit
        :return: None
        """
        self.controller.delete_habit()
        print_end()

    def show_habits_table(self):
        """
        calls the controller to show the habits table
        :return: None
        """
        self.controller.show_habits_table()
        print_end()

    def show_habit_names(self):
        """
        calls the controller to show the habit names
        :return: None
        """
        self.controller.show_habit_names()
        print_end()

    def show_completed_within_last_week(self):
        """
        calls the controller to show the completed habits last week
        :return: None
        """
        self.controller.show_completed_within_last_week()
        print_end()

    def show_longest_streak(self):
        """
        calls the controller to show the longest streak
        :return: None
        """
        self.controller.show_longest_streak()
        print_end()

    def show_longest_streak_habit(self):
        """
        calls the controller to show the longest streak for a habit
        :return: None
        """
        self.controller.show_longest_streak_habit()
        print_end()

    def show_habits_frequency(self):
        """
        calls the controller to show the habits with a certain frequency
        :return: None
        """
        self.controller.show_habits_frequency()
        print_end()

    def complete_habit(self):
        """
        calls the controller to complete a habit
        :return: None
        """
        self.controller.complete_habit()
        print_end()

    def insert_sample_data(self):
        """
        calls the controller to insert sample data
        :return: None
        """
        self.controller.insert_sample_data()
        print_end()

    def clear_database(self):
        """
        calls the controller to clear the database. This is for testing purposes only.
        Drops all tables.
        :return: None
        """
        self.controller.clear_database()
        print_end()

    def get_new_habit_info_from_user(self):
        """
        gets the habit info from the user
        :return: Habit object
        """
        name = input("please enter the name of the habit: ")
        while True:
            frequency = input("please enter the frequency of the habit in full days (e.g. 1 = daily; 7 = weekly): ")
            try:
                frequency = int(frequency)
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        return Habit(name, frequency)

    def get_habit_from_user(self):
        """
        gets the habit info from the user
        :return: Habit object
        """
        name = input("please enter the name of the habit: ")
        return Habit(name)


def print_end():
    """
    Prints a line of dashes.
    :return: None
     """
    print('─' * 150)
