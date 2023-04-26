# Habit Tracker

This is a python application that uses a CLI and sqlite3 database to enable the user to keep track of habits.

## Description

The HabitTracker application is designed to help users develop and maintain good habits by
providing a way to track their progress. The application allows users to create new habits, mark
habits as completed, and view their progress over time. The application uses a Model-ViewController (MVC) architecture to separate the user interface, data storage, and application logic.

## Architecture

This application uses a Model-View-Controller (MVC) architecture. The Model-View-Controller (MVC) 
pattern is a design pattern used in software development that separates the application into three 
interconnected components Model, View and Controller. 
This pattern separates the concerns of the application into three components, allowing
each to operate independently and minimizing the coupling between the components. This
separation makes the code easier to maintain and modify over time, as changes to one component
do not affect the others.

## Features

* add habit: The user can create new habits by entering the name of the habit and the frequency
with which they want to complete the habit (e.g. daily, weekly, monthly).
* delete habit: The user can delete a selected habit.
* complete habit: The user can mark habits as completed by selecting the habit. The habit will
then be updated with the actual timestamp and the streak values are updated (ongoing streak, longest streak, is completed). The counter for the ongoing streak will be set.
* show all habits: This feature shows all the habits that exist in the database.
* show longest streaks: This feature displays the longest streaks for all habits.
* show longest streak for habit: This feature presents the longest streak of a habit specified by
the user.
* show habits with given frequency: This feature displays all habits for a given frequency.
* show habit names: This feature displays all habit names in a list.
* show all habits completed in the last week: This feature shows the list of habit names that have been completed within the last week (calculated from today).
* insert sample data: For testing purposes the user can insert sample data, which provides sample
data for at least five habits with different frequencies.
* clear data: The user has the possibility to wipe all the saved data in the database.

## Getting Started

### Dependencies

```
Python 3.9+
pytest==7.3.0
tabulate==0.9.0
datetime==4.3
```


### Installing


```
gh repo clone KonradKlein91/Habit_Tracker
pip install -r requirements.txt
```

### Executing program

```
python main.py
```
### Run tests

```
pytest test_habittracker.py
```
