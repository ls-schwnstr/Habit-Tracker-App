from Analytics import compute_new_streak
from db import add_user, get_db, add_habit, add_habit_progress, get_tickable_habits_list, \
    get_habits_with_same_periodicity, get_longest_streak, get_longest_streak_total, get_current_streak
from freezegun import freeze_time


class TestUserClass:

    def setup_method(self):
        """
        A function used to set up the test database, test users and test data
        """
        self.db = get_db("test.db")

        add_user(self.db, 'Max', 'Müller', 'mail1@gmail.com', 12345)
        add_user(self.db, 'Lena', 'Schmidt', 'mail2@icloud.com', 11111)

        add_habit(self.db, 'Jogging', 'One session of 30 minutes jogging per week', 'sport', 'weekly',
                  'mail1@gmail.com', '01.11.2022')
        add_habit(self.db, 'Morning Yoga', 'Start the day with ten rounds of Surya Namaskar', 'sport', 'daily',
                  'mail1@gmail.com', '01.11.2022')
        add_habit(self.db, 'Practicing spanish', 'Learn twenty new spanish words', 'education', 'weekly',
                  'mail1@gmail.com', '01.11.2022')
        add_habit(self.db, 'Makramee', 'One hour of knotting', 'creativity', 'weekly', 'mail2@icloud.com', '01.11.2022')
        add_habit(self.db, 'Drinking 2 liters of water', 'Drinking at least two liters of water every day', 'nutrition',
                  'daily', 'mail2@icloud.com', '01.11.2022')

        add_habit_progress(self.db, 'Jogging', 'mail1@gmail.com', 'yes', 1, '10:05:10', '01/11/2022', 2022, 44)
        add_habit_progress(self.db, 'Jogging', 'mail1@gmail.com', 'yes', 2, '12:25:20', '11/09/22', 2022, 45)
        add_habit_progress(self.db, 'Jogging', 'mail1@gmail.com', 'no', 0, '22:04:10', '11/20/22', 2022, 46)
        add_habit_progress(self.db, 'Jogging', 'mail1@gmail.com', 'yes', 1, '18:01:11', '11/23/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 1, '08:25:20', '11/01/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 2, '08:30:20', '11/02/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 3, '08:34:20', '11/03/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 4, '08:21:20', '11/04/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 5, '08:15:20', '11/05/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'no', 0, '08:35:20', '11/06/22', 2022, 44)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 1, '08:22:20', '11/07/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 2, '08:27:20', '11/08/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 3, '08:11:20', '11/09/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 4, '08:25:20', '11/10/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 5, '08:13:20', '11/11/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 6, '08:25:20', '11/12/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 7, '08:22:20', '11/13/22', 2022, 45)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 8, '08:11:20', '11/14/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 9, '08:13:20', '11/15/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 10, '08:44:20', '11/16/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'no', 0, '08:43:20', '11/17/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 1, '08:25:20', '11/18/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 2, '08:22:20', '11/19/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 3, '08:25:20', '11/20/22', 2022, 46)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 4, '08:22:20', '11/21/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 5, '08:26:20', '11/22/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 6, '08:55:20', '11/23/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 7, '08:44:20', '11/24/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 8, '08:34:20', '11/25/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 9, '08:25:20', '11/26/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 10, '08:32:20', '11/27/22', 2022, 47)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 11, '08:13:20', '11/28/22', 2022, 48)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 12, '08:42:20', '11/29/22', 2022, 48)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 13, '08:22:20', '11/30/22', 2022, 48)
        add_habit_progress(self.db, 'Morning Yoga', 'mail1@gmail.com', 'yes', 14, '08:11:20', '12/01/22', 2022, 48)
        add_habit_progress(self.db, 'Practicing spanish', 'mail1@gmail.com', 'yes', 1, '10:05:10', '11/04/22', 2022, 44)
        add_habit_progress(self.db, 'Practicing spanish', 'mail1@gmail.com', 'yes', 2, '12:25:20', '11/08/22', 2022, 45)
        add_habit_progress(self.db, 'Practicing spanish', 'mail1@gmail.com', 'no', 3, '22:04:10', '11/19/22', 2022, 46)
        add_habit_progress(self.db, 'Practicing spanish', 'mail1@gmail.com', 'yes', 4, '18:01:11', '11/23/22', 2022, 47)
        add_habit_progress(self.db, 'Makramee', 'mail2@icloud.com', 'yes', 1, '10:05:10', '11/06/22', 2022, 44)
        add_habit_progress(self.db, 'Makramee', 'mail2@icloud.com', 'yes', 2, '18:11:20', '11/09/22', 2022, 45)
        add_habit_progress(self.db, 'Makramee', 'mail2@icloud.com', 'no', 0, '11:04:10', '11/14/22', 2022, 46)
        add_habit_progress(self.db, 'Makramee', 'mail2@icloud.com', 'yes', 1, '09:01:11', '11/25/22', 2022, 47)
        add_habit_progress(self.db, 'Makramee', 'mail2@icloud.com', 'yes', 1, '10:01:11', '11/28/22', 2022, 48)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 1, '08:25:20', '11/01/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 0, '08:30:20', '11/02/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 1, '08:34:20', '11/03/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 2, '08:21:20', '11/04/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 3, '08:15:20', '11/05/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 0, '08:35:20', '11/06/22',
                           2022, 44)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 1, '08:22:20', '11/07/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 2, '08:27:20', '11/08/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 3, '08:11:20', '11/09/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 4, '08:25:20', '11/10/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 1, '08:13:20', '11/11/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 2, '08:25:20', '11/12022',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 3, '08:22:20', '11/13/22',
                           2022, 45)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 4, '08:11:20', '11/14/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 5, '08:13:20', '11/15/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 0, '08:44:20', '11/16/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 0, '08:43:20', '11/17/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 1, '08:25:20', '11/18/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 2, '08:22:20', '11/19/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 3, '08:25:20', '11/20/22',
                           2022, 46)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 4, '08:22:20', '11/21/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 5, '08:26:20', '11/22/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 6, '08:55:20', '11/23/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 7, '08:44:20', '11/24/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 8, '08:34:20', '11/25/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 9, '08:25:20', '11/26/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'no', 0, '08:32:20', '11/27/22',
                           2022, 47)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 1, '08:13:20', '11/28/22',
                           2022, 48)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 2, '08:42:20', '11/29/22',
                           2022, 48)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 3, '08:22:20', '11/30/22',
                           2022, 48)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 4, '08:11:20', '12/01/22',
                           2022, 48)
        add_habit_progress(self.db, 'Drinking 2 liters of water', 'mail2@icloud.com', 'yes', 5, '08:52:20', '12/02/22',
                           2022, 48)

    # test if all habits can be ticked off, that have not been ticked off yet this day / week
    def test_habit_tick_off_one(self):
        user_data = [('Max', 'Müller', 'mail1@gmail.com', '12345')]
        habit_tick_off_list = get_tickable_habits_list(self.db, user_data)
        tickable_habits = [('Jogging',), ('Morning Yoga',), ('Practicing spanish',)]
        assert tickable_habits == habit_tick_off_list

        user_data = [('Lena', 'Schmidt', 'mail2@icloud.com', '11111')]
        habit_tick_off_list = get_tickable_habits_list(self.db, user_data)
        tickable_habits = [('Makramee',), ('Drinking 2 liters of water',)]
        assert tickable_habits == habit_tick_off_list

    # test if all weekly habits can be ticked off, that have been ticked this week with a 'no' so far
    @freeze_time('2022-11-20')
    def test_habit_tick_off_two(self):
        user_data = [('Max', 'Müller', 'mail1@gmail.com', '12345')]
        habit_tick_off_list = get_tickable_habits_list(self.db, user_data)
        tickable_habits = [('Jogging',), ('Practicing spanish',)]
        assert tickable_habits == habit_tick_off_list

    # test if habits cannot be ticked off, that have been ticked off yet with a 'yes' today (for daily habits)
    # or this week (for weekly habits)
    @freeze_time('2022-11-29 09:00:20')
    def test_habit_tick_off_three(self):
        user_data = [('Lena', 'Schmidt', 'mail2@icloud.com', '11111')]
        habit_tick_off_list = get_tickable_habits_list(self.db, user_data)
        tickable_habits = []
        assert tickable_habits == habit_tick_off_list

    # test if streak is set to 1 if the user ticks off the habit with a 'yes', but the last 'yes' has been too long ago
    @freeze_time('2022-12-29 09:00:20')
    def test_compute_new_streak_one(self):
        user_email = 'mail1@gmail.com'
        habit_name_tick_off = 'Jogging'
        tick_off_type = 'yes'
        new_streak = compute_new_streak(self.db, user_email, habit_name_tick_off, tick_off_type)
        assert new_streak == 1

    # test if streak is raised up by 1 if the user ticks off the habit with a 'yes'
    @freeze_time('2022-12-02')
    def test_compute_new_streak_two(self):
        user_email = 'mail1@gmail.com'
        habit_name_tick_off = 'Morning Yoga'
        tick_off_type = 'yes'
        new_streak = compute_new_streak(self.db, user_email, habit_name_tick_off, tick_off_type)
        assert new_streak == 15

    # test if streak remains the same when the user ticks off the habit with a 'no', but he / she still has time to
    # complete it in the given time period
    @freeze_time('2022-11-30')
    def test_compute_new_streak_three(self):
        user_email = 'mail1@gmail.com'
        habit_name_tick_off = 'Practicing spanish'
        tick_off_type = 'no'
        new_streak = compute_new_streak(self.db, user_email, habit_name_tick_off, tick_off_type)
        assert new_streak == 4

    # test if streak is set to 0 when the user ticks off the habit with a 'no' and the last time he / she has completed
    # the habit successfully has been too long ago
    def test_compute_new_streak_four(self):
        user_email = 'mail2@icloud.com'
        habit_name_tick_off = 'Drinking 2 liters of water'
        tick_off_type = 'no'
        new_streak = compute_new_streak(self.db, user_email, habit_name_tick_off, tick_off_type)
        assert new_streak == 0

    # test if all habits are listed with the pre chosen periodicity
    def test_get_habits_with_same_periodicity(self):
        user_email = 'mail2@icloud.com'
        selected_periodicity = 'daily'
        habit_list = get_habits_with_same_periodicity(self.db, user_email, selected_periodicity)
        assert habit_list == [('Drinking 2 liters of water',)]

    # test if the longest streak for each habit is returned
    def test_get_longest_streak(self):
        user_email = 'mail2@icloud.com'
        habit_list = get_longest_streak(self.db, user_email)
        assert habit_list == [('Drinking 2 liters of water', 9), ('Makramee', 2)]

    # test if the longest streak in total is returned
    def test_get_longest_streak_total(self):
        user_email = 'mail2@icloud.com'
        habit_list = get_longest_streak_total(self.db, user_email)
        assert habit_list == [('Drinking 2 liters of water', 9)]

    # test if the current streak for each habit is returned
    def test_get_current_streak(self):
        user_email = 'mail1@gmail.com'
        habit_list = get_current_streak(self.db, user_email)
        assert habit_list == [('Jogging', '11/23/22', '11/23/22', 1), ('Morning Yoga', '12/01/22', '12/01/22', 14),
                              ('Practicing spanish', '11/23/22', '11/23/22', 4)]

    def teardown_method(self):
        import os
        os.remove("test.db")
