import sqlite3
from datetime import date
from sqlite3 import Error
from time import strftime


def get_db(db_file="main.db"):
    """
    creation of a database connection to the SQLite database main.db
    :param db_file: database file
    :return: Connection object db or None
    """
    db = None
    try:
        db = sqlite3.connect(db_file)
        create_tables(db)
        return db
    except Error as e:
        print(e)

    return db


def create_tables(db):
    """
    creation of the tables users, habits and habits_analysis
    :param db: connection object
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        firstname text NOT NULL,
        lastname text NOT NULL,
        email text PRIMARY KEY NOT NULL,
        password text NOT NULL);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
            habit_name text,
            description text,
            category text,
            frequency text,
            user_email text,
            creation_date text,
            FOREIGN KEY (user_email) REFERENCES users (email)
            );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habits_analysis (
            habit_name text,
            user_email text,
            tick_off_time int,
            tick_off_date int,
            tick_off_year int,
            tick_off_week int,
            tick_off_type text,
            streak int,
            FOREIGN KEY (user_email) REFERENCES users (email),
            FOREIGN KEY (habit_name) REFERENCES habits (habit_name)
            );""")

    db.commit()


def add_user(db, firstname, lastname, email, password):
    """
    A function used to add a new user to the database table users
    :param db: connection object
    :param firstname: user's firstname
    :param lastname: user's lastname
    :param email: user's email address
    :param password: user's password
    """
    cur = db.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (firstname, lastname, email, password))
    db.commit()


def add_habit(db, habit_name, description, category, frequency, user_email, creation_date=None):
    """
    A function used to add a new habit to the database table habits
    :param db: connection object
    :param habit_name: name of the habit
    :param description: description of the habit
    :param category: category the habit belongs to
    :param frequency: frequency at which the habit has to be ticked off
    :param user_email: the email address of the user the habit belongs to
    :param creation_date: creation date of the habit
    """
    cur = db.cursor()
    if not creation_date:
        creation_date = date.today()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?)", (habit_name, description, category, frequency,
                                                                 user_email, creation_date))
    db.commit()


def add_habit_progress_default(db, habit_name, user_email):
    """
    A function used to add a default row to the table habits_analysis with streak set to zero whenever a new
    habit is being created in the habits table.
    param db: connection object
    :param db:
    :param habit_name: name of the habit
    :param user_email: the email address of the user the habit belongs to
    """
    cur = db.cursor()
    streak = 0
    tick_off_time = strftime('%X')
    tick_off_date = strftime('%x')
    tick_off_week = strftime("%W")
    tick_off_year = strftime("%Y")
    tick_off_type = "default"
    cur.execute("INSERT INTO habits_analysis VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (habit_name, user_email, tick_off_time, tick_off_date, tick_off_year, tick_off_week, tick_off_type,
                 streak))
    db.commit()


def add_habit_progress(db, habit_name, user_email, tick_off_type, streak, tick_off_time=None, tick_off_date=None,
                       tick_off_year=None, tick_off_week=None, ):
    """
    A function used to add the progress of a habit to the table habits_analysis. Each time a user ticks off a habit,
    no matter if he/she clicks yes or no, a new row is being created in the table.
    param tick_off_date:
    :param tick_off_week:
    :param tick_off_year:
    :param tick_off_date:
    :param tick_off_time:
    :param db: connection object
    :param habit_name: name of the habit
    :param user_email: email address of the user the habit belongs to
    :param tick_off_type: set to yes, when the habit has been fulfilled, no when the habit has not been fulfilled
    :param streak: the count of the current streak
    """
    cur = db.cursor()
    if not tick_off_time:
        tick_off_time = strftime('%X')
    if not tick_off_date:
        tick_off_date = strftime('%x')
    if not tick_off_year:
        tick_off_year = strftime("%Y")
    if not tick_off_week:
        tick_off_week = strftime("%W")
    cur.execute("INSERT INTO habits_analysis VALUES (?, ?, ?, ?, ?, ?, ?,?)", (habit_name, user_email, tick_off_time,
                                                                               tick_off_date, tick_off_year,
                                                                               tick_off_week, tick_off_type, streak))
    db.commit()


def get_user_data(db, email):
    """
    Retrieves the data from the table users for a certain user based on his/her email-address
    :param db: connection object
    :param email: user's email address
    :return: the user's credentials
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    return cur.fetchall()


def get_habit_data(db, habit_name, user_email):
    """
    Retrieves the data from the table habits for a certain user based on his/her email-address and the habit's name
    :param db: connection object
    :param habit_name: the name of the selected habit
    :param user_email: user's email-address
    :return: the selected habit
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE habit_name=? AND user_email=?", (habit_name, user_email,))
    return cur.fetchall()


def get_habit_list(db, user_email):
    """
    Retrieves all habits from the table habits for a certain user based on his/her email-address
    :param db: connection object
    :param user_email: user's email-address
    :return: list with all habits belonging to the current user
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE user_email=?", (user_email,))
    habit_list = cur.fetchall()
    return habit_list


def get_habit_names(db, user_email):
    """
    Retrieves all habit names from the table habits for a certain user based on his/her email-address
    :param db: connection object
    :param user_email: user's email-address
    :return: list with all habits belonging to the current user
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habits WHERE user_email=?", (user_email,))
    habit_list = cur.fetchall()
    return habit_list


def get_tickable_habits_list(db, user_data):
    """
    Retrieves all habits that have not been yet ticked off with a 'yes' in the current time period
    :param user_data: the active user's credentials
    :param db: connection object
    :return: habit_list with all habits that can be ticked off
    """
    cur = db.cursor()
    user_email = user_data[0][2]
    habit_tick_off_list = get_habit_names(db, user_email)
    last_tick_off_date = strftime('%x')
    last_tick_off_week = int(strftime('%W'))

    # Selection of all daily habits that have already been ticked off today with a 'yes'
    # and removing them from the habit_tick_off_list

    cur.execute("SELECT DISTINCT a.habit_name "
                "FROM habits_analysis AS a LEFT JOIN habits "
                "ON a.user_email = habits.user_email "
                "AND a.habit_name = habits.habit_name "
                "WHERE (a.user_email =? AND frequency = 'daily' AND tick_off_date =? AND tick_off_type = 'yes')",
                (user_email, last_tick_off_date,))

    tick_off_list_daily_habits = cur.fetchall()
    for i in tick_off_list_daily_habits:
        habit_tick_off_list.remove(i)

    # Selection of all weekly habits that have already been ticked off this week with a 'yes'
    # and removing them from the habit_tick_off_list

    cur.execute("SELECT DISTINCT a.habit_name "
                "FROM habits_analysis AS a LEFT JOIN habits "
                "ON a.user_email = habits.user_email "
                "AND a.habit_name = habits.habit_name "
                "WHERE (a.user_email =? AND frequency = 'weekly' AND tick_off_week =? AND tick_off_type = 'yes')",
                (user_email, last_tick_off_week,))

    tick_off_list_weekly_habits = cur.fetchall()
    for i in tick_off_list_weekly_habits:
        habit_tick_off_list.remove(i)

    return habit_tick_off_list


def get_habits_with_same_periodicity(db, user_email, selected_periodicity):
    """
    A function used to retrieve all habits belonging to a user with a certain periodicity
    :param db: connection object
    :param user_email: the active user's email-address
    :param selected_periodicity: the periodicity the user has selected
    :return: habit_list with all habits with the selected periodicity
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habits WHERE user_email=? AND frequency =?", (user_email, selected_periodicity))
    habit_list = cur.fetchall()
    return habit_list


def get_longest_streak(db, user_email):
    """
    A function used to retrieve the longest streak for each habit from the database table habits_analysis
    :param db: connection object
    :param user_email: the active user's email-address
    :return: habit_list with the longest streak for each habit belonging to the user
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name, MAX(streak) FROM habits_analysis WHERE user_email=?"
                "GROUP BY habit_name", (user_email,))
    habit_list = cur.fetchall()
    return habit_list


def get_longest_streak_total(db, user_email):
    """
    A function used to retrieve the longest streak in total from the database table habits_analysis
    :param db: connection object
    :param user_email: the actives user's email-address
    :return: habit_list with the longest streak in total belonging to the user
    """
    # the row is selected from the database table 'habits_analysis' with the maximum streak in total
    cur = db.cursor()
    cur.execute("SELECT habit_name, MAX(streak) FROM habits_analysis WHERE user_email=?", (user_email,))
    habit_list = cur.fetchall()
    return habit_list


def get_current_streak(db, user_email):
    """
    A function used to retrieve the current streak for each habit from the database table habits_analysis
    :param db: connection object
    :param user_email: the actives user's email-address
    :return: habit_list with all habits belonging to the user and their current streal
    """
    # for each habit belonging to the current user, the row with the latest tick_off_date is selected from the
    # database table 'habits_analysis'
    cur = db.cursor()
    cur.execute("SELECT habit_name, tick_off_date, MAX(tick_off_date), streak FROM habits_analysis "
                "WHERE user_email=? AND tick_off_date IN("
                "SELECT MAX(tick_off_date) FROM habits_analysis "
                "WHERE user_email=? "
                "GROUP BY habit_name) "
                "GROUP BY habit_name", (user_email, user_email,))
    habit_list = cur.fetchall()
    return habit_list
