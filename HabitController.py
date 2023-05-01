from HabitModel import HabitModel
from Habit import Habit
from Analytics import *


class HabitController:
    """
    Controller class for the Habit application
    """

    def __init__(self, db_connection=None):
        self.model = HabitModel(db_connection)

    def add_habit(self, Habit):
        """
        calls the model to add a habit
        :param Habit: input from the user in the view
        :return: None
        """
        self.model.add_habit(Habit)

    def delete_habit(self):
        """
        Calls the model to get all the habits from the database.
        Then it prints the habits and asks the user to enter the number of the habit to delete.
        Afterwards calls the model to delete the habit.
        :return: None
        """
        # get all habits from the database
        rows = self.model.get_habits()

        # create a list of Habit objects
        habits = []
        for row in rows:
            habit = Habit(row[1], row[3])
            habits.append(habit)

        # print the habits in a formatted way
        for i, habit in enumerate(habits):
            print("{}. {}".format(i + 1, habit.name))

        # ask the user to enter the number of the habit to delete
        try:
            index = int(input("enter the number of the habit to delete: ")) - 1
        except ValueError:
            print("please enter a number")
            index = int(input("enter the number of the habit to delete: ")) - 1

        # select the habit to delete
        try:  # check if the user entered a valid number
            habits = habits[index]
        except IndexError:
            print("either the number you have entered doesn't exist or is not valid!")
            return

        # call the model to delete the habit
        self.model.delete_habit(habits)

    def show_habits_table(self):
        """
        Calls the analysis module to display the habits in a table
        :return: None
        """
        display_table_habits()

    def get_habits(self):
        """
        Calls the model to get all habits from the database.
        :return:
        """
        self.model.get_habits()

    def show_habit_names(self):
        """
        Calls the analysis module to get the habit names.
        :return: None
        """
        get_habit_names()

    def show_completed_within_last_week(self):
        """
        Calls the analysis module to get the completed habits last week and then prints them.
        :return: None
        """
        show_completed_within_last_week()

    def show_longest_streak(self):
        """
        Calls the analysis module to get the longest streak and then prints it.
        :return: None
        """
        show_longest_streak()

    def show_longest_streak_habit(self):
        """
        Calls the analysis module to get the longest streak for a habit and then prints it.
        :return: None
        """
        show_longest_streak_habit()

    def show_habits_frequency(self):
        """
        Calls the analysis module to get the habits with a certain frequency and then prints them.
        :return: None
        """
        show_habits_frequency()

    def complete_habit(self):
        """
        Calls the model to get all habits and then asks the user to select one to complete.
        Afterwards calls the models to complete the habit.
        :return: None
        """
        # get all habits from the database
        rows = self.model.get_habits()

        # create a list of Habit objects
        habits = []
        for row in rows:
            habit = Habit(row[1], row[2])
            habits.append(habit)

        # print the habits in a formatted way
        for i, habit in enumerate(habits):
            print("{}. {}".format(i + 1, habit.name))

        # ask the user to enter the number of the habit to complete
        index = int(input("enter the number of the habit to complete: ")) - 1

        # complete the habit if the index is valid
        if 0 <= index < len(habits):
            self.model.complete_habit(habits[index])
        else:
            print("either the number you have entered doesn't exist or is not valid!")

    def insert_sample_data(self):
        """
        calls the model to insert sample data
        :return: None
        """
        self.model.insert_sample_data()

    def clear_database(self):
        """
        clears the database and recreates the tables
        :return: None
        """
        # clear the database
        clear_database()

        # recreate the tables
        self.model.recreate_tables()
