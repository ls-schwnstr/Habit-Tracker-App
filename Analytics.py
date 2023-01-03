from datetime import datetime, timedelta
from time import strftime
import questionary
from db import add_habit_progress, get_db, get_habit_list, get_habits_with_same_periodicity, get_longest_streak, \
    get_longest_streak_total, get_current_streak


class HabitAnalytics:
    """
    A class used to represent the progress for each habit the user has created.

    """

    def __init__(self, habit_name: str, user_email: str, tick_off_time: str, tick_off_date: str, tick_off_year: str,
                 tick_off_week: str):
        """
        The init method.
        param habit_name: the name of the habit
        :param user_email: the user's email the habit belongs to
        :param tick_off_time: the time the user completed the habit
        :param tick_off_date: the day the user completed the habit
        :param tick_off_year: the year the user completed the habit
        :param tick_off_week: the week the user completed the habit
        """
        self.habit_name = habit_name
        self.user_email = user_email
        self.tick_off_time = tick_off_time
        self.tick_off_date = tick_off_date
        self.tick_off_year = tick_off_year
        self.tick_off_week = tick_off_week
        self.streak = 0

    def __getitem__(self, user_email):
        """
        A function used for accessing the list item user_email
        :param user_email: the email-address of the current user
        :return: user_email
        """
        return getattr(self, user_email)

    def __str__(self):
        """
        A function used to represent the class objects as a string
        :return: string of the class object
        """
        return f"{self.habit_name}: {self.streak}"

    def store(self, db):
        """
        A function used to store the habit name, user's email, the tick-off time and the current streak in the
        database table 'habits_analysis'
        :param db: connection object
        """
        add_habit_progress(db, self.habit_name, self.user_email, self.tick_off_time, self.streak)


def compute_new_streak(db, user_email, habit_name_tick_off, tick_off_type):
    """
    A function used to compute the new streak of the user's selected habit
    :param db: connection object
    :param user_email: the active user's email-address
    :param habit_name_tick_off: the habit that the user ticks off
    :param tick_off_type: 'yes' if the user has completed the habit, 'no' if he has not yet completed the habit
    :return: the new streak
    """
    cur = db.cursor()
    current_tick_off_date = strftime('%x')
    today = datetime.strptime(current_tick_off_date, '%x')
    current_tick_off_week = int(strftime('%W'))

    if tick_off_type == 'yes':
        # Selection of the latest row in the database table 'habits_analysis' where the user has ticked off
        # the habit with 'yes'
        cur.execute("SELECT a.habit_name, MAX(tick_off_date), streak, frequency, tick_off_week "
                    "FROM habits_analysis AS a LEFT JOIN habits "
                    "ON a.user_email = habits.user_email AND a.habit_name = habits.habit_name  "
                    "WHERE a.user_email=? AND a.habit_name =? "
                    "AND (tick_off_type IN('yes', 'default'))", (user_email, habit_name_tick_off))

        records = cur.fetchall()
        day_string = str(records[0][1])
        last_week_completed = int(records[0][4])
        last_day_completed = datetime.strptime(day_string, '%m/%d/%y')
        frequency = records[0][3]
        streak = records[0][2]

        if frequency == 'daily':
            # check if the last time the daily habit has been completed, was one day ago
            if today - last_day_completed <= timedelta(days=1):
                # the streak is increased by 1
                streak = streak + 1
                try:
                    return streak
                finally:
                    pass
            else:
                # the streak is set to 1 because the last time the habit has been completed, was more than
                # one day ago
                streak = 1
                try:
                    return streak
                finally:
                    pass

        if frequency == 'weekly':
            # check if the last time the weekly habit has been completed, was the previous calendar week
            if current_tick_off_week - last_week_completed <= 1:
                # the streak is increased by 1
                streak = streak + 1
                try:
                    return streak
                finally:
                    pass
            else:
                # the streak is set to 1 because the last time the habit has been completed, was more than
                # one week ago
                streak = 1
                try:
                    return streak
                finally:
                    pass

    if tick_off_type == "no":
        # Selection of the latest row in the database table 'habits_analysis' where the user had
        # successfully completed the habit
        cur.execute("SELECT a.habit_name, MAX(tick_off_date), streak, frequency, tick_off_week"
                    " FROM habits_analysis AS a LEFT JOIN habits "
                    "ON a.user_email = habits.user_email AND a.habit_name = habits.habit_name  "
                    "WHERE a.user_email=? AND a.habit_name =? AND (tick_off_type IN('yes', 'default'))",
                    (user_email, habit_name_tick_off))
        records = cur.fetchall()
        day_string = str(records[0][1])
        last_week_completed = int(records[0][4])
        last_day_completed = datetime.strptime(day_string, '%m/%d/%y')
        frequency = records[0][3]

        if frequency == 'daily':
            # check if the last successful completion was yesterday. if so, the user still has time to
            # complete the habit later this day.
            if today - last_day_completed <= timedelta(days=1):
                # the streak remains the same.
                streak = records[0][2]
                try:
                    return streak
                finally:
                    pass
            else:
                # if the last successful completion was more than one day ago, the streak is reset to zero.
                streak = 0
                try:
                    return streak
                finally:
                    pass

        if frequency == 'weekly':
            # check if the last successful completion was last week. if so, the user still has time to
            # complete the habit later this week.
            if current_tick_off_week - last_week_completed <= 1:
                streak = records[0][2]
                try:
                    return streak
                finally:
                    pass
            else:
                # if the last successful completion was more than one week ago, the streak is reset to zero.
                streak = 0
                try:
                    return streak
                finally:
                    pass

        else:
            pass


def habit_progress_confirmation(db, user_data, habit_tick_off_list):
    """
    A function used to confirm whether the habit has been fulfilled or not
    """
    user_email = user_data[0][2]

    # the names of the habits that can be ticked off today are retrieved from the 'habit_tick_off_list'
    for row in habit_tick_off_list:
        habit_name_tick_off = row[0]

        # user has to specify for each habit whether he / she has completed the habit or not.
        tick_off_confirmation = questionary.confirm("Have you done the habit " + habit_name_tick_off + "?").ask()

        if tick_off_confirmation:
            new_tick_off_type = "yes"
            # function 'compute_new_streak' is called to compute the new streak
            new_streak = compute_new_streak(db, user_email, habit_name_tick_off, new_tick_off_type)
            # A new row is added to the database table 'habits_analysis' with the new streak.
            add_habit_progress(db, habit_name_tick_off, user_email, new_tick_off_type, new_streak)

        else:
            new_tick_off_type = "no"
            new_streak = compute_new_streak(db, user_email, habit_name_tick_off, new_tick_off_type)
            add_habit_progress(db, habit_name_tick_off, user_email, new_tick_off_type, new_streak)


def habit_analysis(self):
    """
    A function used to analyze the habit progress.
    """
    analytics_overview = ''

    while analytics_overview != 'go back to overview':
        db = get_db()
        user_email = self[0][2]
        analytics_overview = questionary.select("What do you want to analyze?",
                                                choices=[
                                                    'show habits with same periodicity',
                                                    'show longest streak for a habit',
                                                    'show longest streak in total',
                                                    'show current streak for each habit',
                                                    'show all currently tracked habits',
                                                    'go back to overview'
                                                ],
                                                ).ask()

        if analytics_overview == 'show habits with same periodicity':
            selected_periodicity = questionary.select("Which periodicity do you want to select?",
                                                      choices=[
                                                          'daily',
                                                          'weekly'
                                                      ],
                                                      ).ask()

            # all habits belonging to the current user are selected based on the chosen periodicity.
            habit_list = get_habits_with_same_periodicity(db, user_email, selected_periodicity)

            print('These are your ' + selected_periodicity + ' habits:')
            print(habit_list)


        if analytics_overview == 'show longest streak for a habit':
            # for each habit belonging to the current user, the row with the maximum streak is selected from the
            # database table 'habits_analysis'
            habit_list = get_longest_streak(db, user_email)

            for i in habit_list:
                habit_name = i[0]
                streak = i[1]
                print('This is your longest streak for the habit ' + str(habit_name) + ': ' + str(streak))

        if analytics_overview == 'show longest streak in total':
            # the habit with the longest streak in total is selected from the database table 'habits_analysis'
            habit_list = get_longest_streak_total(db, user_email)
            habit_name = habit_list[0][0]
            streak = habit_list[0][1]
            print('Your longest streak in total is the habit ' + str(habit_name) + ' with a streak of ' + str(streak) +
                  ' times!')

        if analytics_overview == 'show current streak for each habit':
            # for each habit the newest row is selected from the database table 'habits_analysis'
            habit_list = get_current_streak(db, user_email)
            for i in habit_list:
                habit_name = i[0]
                streak = i[3]
                print('This is your current streak for the habit ' + str(habit_name) + ': ' + str(streak))

        if analytics_overview == 'show all currently tracked habits':
            # all habits belonging to the user are selected from the database table 'habits'
            records = get_habit_list(db, user_email)

            print('These are your currently tracked habits:')

            for i in records:
                habit_name = i[0]
                description = i[1]
                category = i[2]
                frequency = i[3]
                print('habit: ' + str(habit_name) + ' description: ' + str(description) + ' category: ' + str(category)
                      + ' frequency: ' + str(frequency))

        if analytics_overview == 'go back to overview':
            pass

    return False
