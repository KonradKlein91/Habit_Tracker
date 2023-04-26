import datetime


class Habit:
    """
    A class used to represent a habit

    ...

    Attributes
    ----------

    name : str
        name of the habit
    created_at : str
        date and time when the habit was created
    frequency : int
        frequency of the habit in days
    is_completed : bool
        whether the habit has been completed today (default: False)
    ongoing_streak : int
        number of ongoing times the habit has been completed (default: 0)
    longest_streak : int
        the longest streak reached for the habit (default: 0)
    last_completed_at : str
        date and time when the habit was last completed (default: None)
    """

    def __init__(self, name, frequency):
        self.id = None
        self.name = name
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.frequency = frequency
        self.is_completed = False
        self.ongoing_streak = 0
        self.longest_streak = 0
        self.last_completed_at = None



