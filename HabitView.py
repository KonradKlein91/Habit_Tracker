from Habit import Habit
from HabitController import HabitController


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
            choice = input("enter your choice: ")
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
        print("-----------------------")
        print("1. add a new habit")
        print("2. delete a habit")
        print("3. complete a habit")
        print("4. show all habits")
        print("5. show longest streaks")
        print("6. show longest streak for a habit")
        print("7. show habits with certain frequency")
        print("8. show habit names")
        print("9. show completed habits last week")
        print("10. insert sample data")
        print("11. clear database")
        print("q. quit")
        print("-----------------------")

    def add_habit(self):
        """
        gets the new habit info from the user and calls the controller to add the habit
        :return: None
        """
        Habit = self.get_new_habit_info_from_user()
        self.controller.add_habit(Habit)


    def delete_habit(self):
        """
        calls the controller to delete the habit
        :return: None
        """
        self.controller.delete_habit()

    def show_habits_table(self):
        """
        calls the controller to show the habits table
        :return: None
        """
        self.controller.show_habits_table()

    def show_habit_names(self):
        """
        calls the controller to show the habit names
        :return: None
        """
        self.controller.show_habit_names()

    def show_completed_within_last_week(self):
        """
        calls the controller to show the completed habits last week
        :return: None
        """
        self.controller.show_completed_within_last_week()

    def show_longest_streak(self):
        """
        calls the controller to show the longest streak
        :return: None
        """
        self.controller.show_longest_streak()

    def show_longest_streak_habit(self):
        """
        calls the controller to show the longest streak for a habit
        :return: None
        """
        self.controller.show_longest_streak_habit()

    def show_habits_frequency(self):
        """
        calls the controller to show the habits with a certain frequency
        :return: None
        """
        self.controller.show_habits_frequency()

    def complete_habit(self):
        """
        calls the controller to complete a habit
        :return: None
        """
        self.controller.complete_habit()

    def insert_sample_data(self):
        """
        calls the controller to insert sample data
        :return: None
        """
        self.controller.insert_sample_data()

    def clear_database(self):
        """
        calls the controller to clear the database. This is for testing purposes only.
        Drops all tables.
        :return: None
        """
        self.controller.clear_database()

    def get_new_habit_info_from_user(self):
        """
        gets the habit info from the user
        :return: Habit object
        """
        name = input("enter the name of the habit: ")
        while True:
            frequency = input("Enter the frequency of the habit in full days (e.g. 1 = daily; 7 = weekly): ")
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
        name = input("enter the name of the habit: ")
        return Habit(name)