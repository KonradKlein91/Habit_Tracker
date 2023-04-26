import sqlite3
import datetime
import Habit


class HabitModel:

    def __init__(self, db_connection=None):
        """
        Model for the Habit application
        """
        if db_connection is not None:
            self.conn = db_connection
        else:
            self.conn = sqlite3.connect('habits.db')
            self.conn.execute("PRAGMA foreign_keys=1")  # enable foreign key constraints
            self.conn.execute("CREATE TABLE IF NOT EXISTS habits (id integer PRIMARY KEY AUTOINCREMENT, "
                              "                                   name text, "
                              "                                   created_at date, "
                              "                                   frequency int, "
                              "                                   is_completed int, "
                              "                                   ongoing_streak int, "
                              "                                   longest_streak int, "
                              "                                   last_completed_at text)"
                              )
            self.conn.execute("CREATE TABLE IF NOT EXISTS habit_logs (id integer PRIMARY KEY AUTOINCREMENT, "
                              "                                       habit_id int, "
                              "                                       completed_at date,"
                              "                                       CONSTRAINT FK_habits "
                              "                                       FOREIGN KEY (habit_id) REFERENCES habits(id)"
                              "                                       ON DELETE CASCADE)"
                              )

    def recreate_tables(self):
        """
        recreate the tables in the database
        :return: None
        """
        self.conn.execute("PRAGMA foreign_keys=1")  # enable foreign key constraints
        self.conn.execute("CREATE TABLE IF NOT EXISTS habits (id integer PRIMARY KEY AUTOINCREMENT, "
                          "                                   name text, "
                          "                                   created_at date, "
                          "                                   frequency int, "
                          "                                   is_completed int, "
                          "                                   ongoing_streak int, "
                          "                                   longest_streak int, "
                          "                                   last_completed_at text)"
                          )
        self.conn.execute("CREATE TABLE IF NOT EXISTS habit_logs (id integer PRIMARY KEY AUTOINCREMENT, "
                          "                                       habit_id int, "
                          "                                       completed_at date,"
                          "                                       CONSTRAINT FK_habits "
                          "                                       FOREIGN KEY (habit_id) REFERENCES habits(id)"
                          "                                       ON DELETE CASCADE)"
                          )

    def get_habits(self):
        """
        Get all habits from the database
        :return: a list of habits
        """
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute("SELECT * FROM habits")
        habits = c.fetchall()
        return habits

    def add_habit(self, habit):
        """
        Create a new Habit object and add it to the database
        :param habit: takes the user input for the habit name and frequency
        :return: None
        """
        self.conn.execute("INSERT INTO habits ( id, "
                          "                     name, "
                          "                     created_at, "
                          "                     frequency, "
                          "                     is_completed, "
                          "                     ongoing_streak, "
                          "                     longest_streak, "
                          "                     last_completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (habit.id, habit.name, habit.created_at, habit.frequency, habit.is_completed,
                           habit.ongoing_streak,
                           habit.longest_streak, habit.last_completed_at))
        self.conn.commit()

    def delete_habit(self, habit):
        """
        Delete a habit from the database
        :param habit: user input which habit to delete
        :return: None
        """
        self.conn.execute("DELETE FROM habits WHERE name = ?", (habit.name,))
        self.conn.commit()

    def complete_habit(self, habit):
        """
        Update the habit table with the current date and update the ongoing_streak and longest_streak
        :param habit: user input which habit to complete
        :return: None
        """
        # get the last_completed_at, ongoing_streak and longest_streak from the habits table for the selected habit
        cursor = self.conn.execute("SELECT  id, "
                                   "        last_completed_at, "
                                   "        ongoing_streak, "
                                   "        longest_streak, "
                                   "        frequency "
                                   "        FROM habits WHERE name = ?", (habit.name,))
        habit_id, last_completed_at, ongoing_streak, longest_streak, frequency = cursor.fetchone()

        # get the current date in different string formats
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # compare the last_completed_at date with the current date
        # do nothing if the habit has already been completed today
        if last_completed_at == today_str:
            pass

        # update the ongoing_streak and longest_streak if last_completed_at is empty
        elif last_completed_at == '':
            ongoing_streak = 1

        # update the ongoing_streak if the last_completed_at date is not empty and the difference between the
        # current date and the last_completed_at date is equal to the frequency
        elif last_completed_at is not None and (
                datetime.datetime.now() - datetime.datetime.strptime(last_completed_at, "%Y-%m-%d")).days == frequency:
            ongoing_streak = ongoing_streak + 1

        # reset the ongoing_streak if streak has been broken
        # (i.e. the difference between today and the last_completed_at is not equal to the frequency)
        else:
            ongoing_streak = 1

        # update the historical longest_streak if the ongoing_streak is higher than the longest streak
        if ongoing_streak > longest_streak:
            longest_streak = ongoing_streak
        else:
            longest_streak = longest_streak

        # update the habits table with the new values
        self.conn.execute(
            "UPDATE habits SET  is_completed = 1, "
            "                   ongoing_streak = ?, "
            "                   longest_streak = ?, "
            "                   last_completed_at = ? "
            "WHERE name = ?", (ongoing_streak, longest_streak, today_str, habit.name))

        # add a completion entry to the habit_logs table
        self.conn.execute("INSERT INTO habit_logs (habit_id, completed_at) VALUES (?, ?)", (habit_id, today_datetime))
        self.conn.commit()

    def insert_sample_data(self):
        """
        Insert sample data into the database
        :return: None
        """
        data = [(1, "Drink Water", "2021-05-01 15:01:36", 1, 0, 0, 0, None),
                (2, "Do Yoga", "2021-05-06 13:25:09", 3, 1, 1, 1, "2021-05-09"),
                (3, "Read a book", "2021-05-07 11:42:03", 2, 0, 0, 0, None),
                (4, "Meditate", "2021-05-10 08:15:42", 1, 0, 0, 0, None),
                (5, "Take a walk", "2021-05-12 17:34:21", 4, 1, 1, 1, "2021-05-16"),
                (6, "Practice guitar", "2021-05-15 14:28:55", 2, 0, 0, 0, None),
                (7, "Write in journal", "2021-05-18 10:57:22", 1, 0, 0, 0, None),
                (8, "Call a friend", "2021-05-20 16:40:19", 3, 1, 2, 2, "2021-05-26"),
                (9, "Cook a new recipe", "2021-05-23 12:12:59", 2, 0, 0, 0, None),
                (10, "Practice Spanish", "2021-05-26 09:38:02", 1, 0, 0, 0, None),
                (11, "Take a break from social media", "2021-05-29 16:20:51", 1, 0, 0, 0, None),
                (12, "Clean the house", "2021-06-01 14:01:37", 4, 1, 1, 1, "2021-06-05"),
                (13, "Stretch", "2021-06-04 11:20:46", 1, 0, 0, 0, None),
                (14, "Try a new hobby", "2021-06-07 09:42:39", 2, 0, 0, 0, None),
                (15, "Listen to a new podcast", "2021-06-10 17:05:12", 1, 0, 0, 0, None),
                (16, "Plan out the week ahead", "2021-06-13 13:44:29", 3, 1, 2, 2, "2021-06-19"),
                (17, "Do something creative", "2021-06-16 10:15:54", 1, 0, 0, 0, None),
                (18, "Take a day trip", "2021-06-19 15:55:37", 2, 0, 0, 0, None),
                (19, "Declutter flat", "2023-04-20 12:30:22", 1, 1, 1, 1, "2023-04-24"),
                (20, "Try a new restaurant", "2021-06-25 08:57:09", 30, 1, 1, 1, "2021-07-25")]

        for row in data:
            self.conn.execute(
                "INSERT INTO habits (   id, "
                "                       name, "
                "                       created_at, "
                "                       frequency, "
                "                       is_completed, "
                "                       ongoing_streak, "
                "                       longest_streak, "
                "                       last_completed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                row
            )

        # TODO - add sample data for habit_logs table
        data_logs = [(1, 2, '2021-05-09 14:19:56'),
                     (2, 5, '2021-05-16 11:05:15'),
                     (3, 8, '2021-05-23 15:47:58'),
                     (4, 8, '2021-05-26 05:25:36'),
                     (5, 12, '2021-06-05 21:07:22'),
                     (6, 16, '2021-06-16 12:49:08'),
                     (7, 16, '2021-06-19 04:30:53'),
                     (8, 20, '2021-07-25 10:04:58'),
                     (9, 19, '2023-04-24 04:30:53')]


        for row in data_logs:
            self.conn.execute(
                "INSERT INTO habit_logs (   id, "
                "                           habit_id, "
                "                           completed_at) "
                "VALUES (?, ?, ?)",
                row
            )

        self.conn.commit()
        self.conn.close()

