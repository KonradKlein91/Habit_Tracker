import pytest
import sqlite3
import datetime
from HabitModel import HabitModel
from Habit import Habit
from HabitController import HabitController


# test create habit user input possibilities: string

@pytest.fixture(scope="module")
def db_connection():
    # create a test database
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=1")  # enable foreign key constraints
    c.execute("CREATE TABLE IF NOT EXISTS habits (id integer PRIMARY KEY AUTOINCREMENT, "
              "                                   name text, "
              "                                   created_at date, "
              "                                   frequency int, "
              "                                   is_completed int, "
              "                                   ongoing_streak int, "
              "                                   longest_streak int, "
              "                                   last_completed_at text)"
              )
    c.execute("CREATE TABLE IF NOT EXISTS habit_logs (id integer PRIMARY KEY AUTOINCREMENT, "
              "                                       habit_id int, "
              "                                       completed_at date,"
              "                                       CONSTRAINT FK_habits "
              "                                       FOREIGN KEY (habit_id) REFERENCES habits(id)"
              "                                       ON DELETE CASCADE)"
              )
    yield conn
    conn.close()


# test create habit user input possibilities: letters
def test_add_habit_str(db_connection):
    # create a habit object
    habit_name = "testhabit"
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    habit_frequency = 1
    habit = Habit(habit_name, habit_frequency)
    HabitController(db_connection).add_habit(habit)

    # check if the habit was added to the database
    c = db_connection.cursor()
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == habit_name
    assert habit[2] == created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 0  # is_completed should default to 0
    assert habit[5] == 0  # ongoing_streak should default to 0
    assert habit[6] == 0  # longest_streak should default to 0
    assert habit[7] is None  # last_completed_at should default to None


# test create habit user input possibilities: integer
def test_add_habit_int(db_connection):
    habit_name = 987
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    habit_frequency = 1

    # create a habit object
    habit = Habit(habit_name, habit_frequency)
    HabitController(db_connection).add_habit(habit)

    # check if the habit was added to the database
    c = db_connection.cursor()
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == str(habit_name)  # input is saved as string in db
    assert habit[2] == created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 0  # is_completed should default to 0
    assert habit[5] == 0  # ongoing_streak should default to 0
    assert habit[6] == 0  # longest_streak should default to 0
    assert habit[7] is None  # last_completed_at should default to None


# test create habit user input possibilities: special characters
def test_add_habit_special(db_connection):
    # input is converted to string
    habit_name = '!"£$%^&*()'
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    habit_frequency = 1

    # create a habit object
    habit = Habit(habit_name, habit_frequency)
    HabitController(db_connection).add_habit(habit)

    # check if the habit was added to the database
    c = db_connection.cursor()
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == habit_name  # input is saved as string in db
    assert habit[2] == created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 0  # is_completed should default to 0
    assert habit[5] == 0  # ongoing_streak should default to 0
    assert habit[6] == 0  # longest_streak should default to 0
    assert habit[7] is None  # last_completed_at should default to None


# test create habit user input possibilities: empty string
def test_add_habit_empty(db_connection):
    # input is converted to string
    habit_name = ''
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    habit_frequency = 1

    # create a habit object
    habit = Habit(habit_name, habit_frequency)
    HabitController(db_connection).add_habit(habit)

    # check if the habit was added to the database
    c = db_connection.cursor()
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == habit_name  # input is saved as string in db
    assert habit[2] == created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 0  # is_completed should default to 0
    assert habit[5] == 0  # ongoing_streak should default to 0
    assert habit[6] == 0  # longest_streak should default to 0
    assert habit[7] is None  # last_completed_at should default to None


def test_complete_habit_daily(db_connection):
    # insert mocking data into temp database
    # daily frequency habit has been created 3 days ago and has been completed twice already
    habit_name = "testhabit_daily"
    habit_frequency = 1
    habit_created_at = (datetime.datetime.now() - datetime.timedelta(days=habit_frequency * 2)).strftime(
        "%Y-%m-%d %H:%M:%S")
    habit_is_completed = 1
    habit_ongoing_streak = 2
    habit_longest_streak = 2
    habit_last_completed_at = (datetime.datetime.now() - datetime.timedelta(days=habit_frequency)).strftime("%Y-%m-%d")

    # create a habit object
    habit = Habit(habit_name, habit_frequency)

    # insert mocking data into temp database
    c = db_connection.cursor()
    c.execute("INSERT INTO habits   ("
              "                     name, "
              "                     created_at, "
              "                     frequency, "
              "                     is_completed, "
              "                     ongoing_streak, "
              "                     longest_streak, "
              "                     last_completed_at"
              "                     ) "
              "VALUES (?, ?, ?, ?, ?, ?, ?)",
              (habit_name,
               habit_created_at,
               habit_frequency,
               habit_is_completed,
               habit_ongoing_streak,
               habit_longest_streak,
               habit_last_completed_at
               )
              )
    db_connection.commit()

    # call the method to complete the habit and check that it is marked as completed
    model = HabitModel(db_connection)
    model.complete_habit(habit)

    # get the habit from the temp database and close the connection
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()

    # get habit_logs from the temp database
    c.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit[0],))
    habit_logs = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == habit_name
    assert habit[2] == habit_created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 1  # is_completed should be set to 1 as habit has been completed successfully
    assert habit[5] == 3  # ongoing_streak should be incremented by 1
    assert habit[6] == 3  # longest_streak should be incremented by 1
    assert habit[7] == datetime.datetime.now().strftime("%Y-%m-%d")
    assert habit_logs is not None


def test_complete_habit_weekly(db_connection):
    # insert mocking data into temp database
    # daily frequency habit has been created 3 days ago and has been completed twice already
    habit_name = "testhabit_weekly"
    habit_frequency = 7
    habit_created_at = (datetime.datetime.now() - datetime.timedelta(days=habit_frequency * 2)).strftime(
        "%Y-%m-%d %H:%M:%S")
    habit_is_completed = 1
    habit_ongoing_streak = 2
    habit_longest_streak = 2
    habit_last_completed_at = (datetime.datetime.now() - datetime.timedelta(days=habit_frequency)).strftime("%Y-%m-%d")

    # create a habit object
    habit = Habit(habit_name, habit_frequency)

    # insert mocking data into temp database
    c = db_connection.cursor()
    c.execute("INSERT INTO habits   ("
              "                     name, "
              "                     created_at, "
              "                     frequency, "
              "                     is_completed, "
              "                     ongoing_streak, "
              "                     longest_streak, "
              "                     last_completed_at"
              "                     ) "
              "VALUES (?, ?, ?, ?, ?, ?, ?)",
              (habit_name,
               habit_created_at,
               habit_frequency,
               habit_is_completed,
               habit_ongoing_streak,
               habit_longest_streak,
               habit_last_completed_at
               )
              )
    db_connection.commit()

    # call the method to complete the habit and check that it is marked as completed
    model = HabitModel(db_connection)
    model.complete_habit(habit)

    # get the habit from the temp database and close the connection
    c.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    habit = c.fetchone()

    # get habit_logs from the temp database
    c.execute("SELECT * FROM habit_logs WHERE habit_id = ?", (habit[0],))
    habit_logs = c.fetchone()
    c.close()

    assert habit is not None
    assert habit[1] == habit_name
    assert habit[2] == habit_created_at
    assert habit[3] == habit_frequency
    assert habit[4] == 1  # is_completed should be set to 1 as habit has been completed successfully
    assert habit[5] == 3  # ongoing_streak should be incremented by 1
    assert habit[6] == 3  # longest_streak should be incremented by 1
    assert habit[7] == datetime.datetime.now().strftime("%Y-%m-%d")
    assert habit_logs is not None
