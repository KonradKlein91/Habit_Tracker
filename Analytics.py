import sqlite3
import datetime
from functools import reduce
from tabulate import tabulate


def display_table_habits():
    """
    Display the habits table in a formatted table
    :return: None
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("SELECT * FROM habits")
    habits = c.fetchall()
    conn.close()
    print(tabulate(habits,
                   headers=["ID", "Name", "Created at", "Frequency", "Completed", "Ongoing streak", "Longest streak",
                            "Last completed at"], tablefmt="fancy_grid"))


def show_habits_frequency():
    """
    Show all habits with a specific frequency
    :return:
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # get the frequency from the user
    frequency = input("Enter the frequency of the habit in full days (e.g. 7 for weekly): ")

    # get the habits with the frequency from the user
    c.execute("SELECT name, frequency FROM habits WHERE frequency = ?", (frequency,))
    habits = c.fetchall()
    conn.close()

    # display the habits with the frequency from the user
    print(tabulate(habits, headers=["Name", "Frequency"], tablefmt="fancy_grid"))


def show_longest_streak():
    """
    Show the longest streak for all habits
    :return: None
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # get the longest streak for all habits
    c.execute("SELECT name, MAX(longest_streak) FROM habits")
    habits = c.fetchall()
    conn.close()

    # display the longest streak for all habits
    print(tabulate(habits, headers=["Name", "Longest streak"], tablefmt="fancy_grid"))


def show_longest_streak_habit():
    """
    Show the longest streak for a specific habit
    :return:
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # get all habits from the database
    c.execute("SELECT name FROM habits")
    show_habits = c.fetchall()

    # show all habits to the user and ask him which habit he wants to see the longest streak for
    print(tabulate(show_habits, headers=["Name"], tablefmt="fancy_grid"))
    name = input("Enter the exact name of the habit: ")

    # get the longest streak for the habit chosen by user
    c.execute("SELECT name, ongoing_streak, longest_streak, last_completed_at FROM habits WHERE name = ?", (name,))
    habits = c.fetchall()
    conn.close()
    # if no habits with this name exist, print a message, else continue
    if len(habits) == 0:
        return print("No habit with this name exists.")
    else:
        print(tabulate(habits, headers=["Name", "Ongoing streak", "Longest streak",
                                        "Last completed at"], tablefmt="fancy_grid"))


def clear_database():
    """
    Drops the table habits and habit_logs.
    :return: None
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("DROP TABLE habits")
    c.execute("DROP TABLE habit_logs")
    print("Database cleared.")


def show_completed_within_last_week():
    """
    Show all habits that have been completed within the last 7 days using the filter function. Prints out a list of
    habit names.. :return: None
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # Get the date 7 days ago
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)

    # Query the habit_logs table for all habit_ids that have been completed within the last 7 days
    c.execute(
        "SELECT habit_id, habits.name, completed_at FROM habit_logs JOIN habits ON habit_logs.habit_id = habits.id")
    habits = c.fetchall()

    # Convert the completed_at column to datetime objects
    habits = [(h[0], h[1], datetime.datetime.strptime(h[2], "%Y-%m-%d %H:%M:%S")) for h in habits]

    # Use the filter function to get all the habits completed within the last week
    habits = list(filter(lambda h: h[2] >= last_week, habits))

    # Use tabulate to display the results
    table_headers = ["Habit ID", "Habit Name", "Completed at"]
    print(tabulate(habits, headers=table_headers, tablefmt="fancy_grid"))
    conn.close()


def get_habit_names():
    """
    Get the names of all habits. Prints a formatted table with the names of all habits.
    :return: None
    """
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("SELECT name FROM habits")
    habits = c.fetchall()

    # use the reduce function to iterate over the list of tuples, and for each tuple,
    # it extracts the name and appends it to the accumulator acc.
    habit_names = reduce(lambda acc, habit: acc + [[habit[0]]], habits, [])
    print(tabulate(habit_names, headers=["Name"], tablefmt="fancy_grid"))
    conn.close()
