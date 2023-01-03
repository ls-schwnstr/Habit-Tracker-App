from datetime import date
import questionary
from db import get_db, add_habit, get_habit_data, get_habit_list, add_habit_progress_default


class HabitClass:

    def __init__(self, habit_name: str, description: str, category: str, frequency: str, user_email: str,
                 creation_date):
        """
        The init function.
        param habit_name: the name of the habit
        :param description: the description of the habit
        :param category: the category the habit belongs to
        :param frequency: the frequency at which the habit has to be completed in order to raise the streak
        :param user_email: the email-address of the user the habit belongs to
        :param creation_date: the creation date of the habit
        """
        self.habit_name = habit_name
        self.description = description
        self.category = category
        self.frequency = frequency
        self.user_email = user_email
        self.creation_date = creation_date

        self.db = get_db()
        self.cur = self.db.cursor()

    def store(self, db):
        """
        A function used to store a new or edited habit in the database.
        param db: connection object
        """
        add_habit(db, self.habit_name, self.description, self.category, self.frequency, self.user_email,
                  self.creation_date)

        add_habit_progress_default(db, self.habit_name, self.user_email)

    def __str__(self):
        """
        A function used to represent the class objects as a string
        :return: string of the class object
        """
        return f"{self.habit_name} {self.description} {self.category} {self.frequency} {self.user_email} " \
               f"{self.creation_date}"

    def __getitem__(self, user_email):
        """
        A function used for accessing the list item user_email
        :param user_email: the email-address of the current user
        :return: user_email
        """
        return getattr(self, user_email)

    def add_predefined_habit(self):
        """
        A function used to enable a new user, who has no habits yet, to choose up to five predefined habits.
        """
        db = get_db()
        user_email = self[0][2]
        creation_date = str(date.today())

        habit_list = get_habit_list(db, user_email)
        # check if habit_list is empty. if so, the predefined habits are shown.
        if len(habit_list) == 0:
            print("You have no habits yet. You can choose from the following predefined habits: ")

            habit_one = questionary.confirm("Habit: Jogging | Frequency: weekly. Do you want to add this habit?"
                                            ).ask()

            if habit_one:
                habit_name = "Jogging"
                description = "One session of 30 minutes jogging per week"
                category = "sport"
                frequency = "weekly"
                new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
                new_habit.store(db)
            else:
                pass

            habit_two = questionary.confirm("Habit: Makramee | Frequency: weekly. Do you want to add this habit?"
                                            ).ask()

            if habit_two:
                habit_name = "Makramee"
                description = "One hour of knotting."
                category = "creativity"
                frequency = "weekly"
                new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
                new_habit.store(db)
            else:
                pass

            habit_three = questionary.confirm("Habit: Drinking 2 liters of water | "
                                              "Frequency: Daily. Do you want to add this habit?"
                                              ).ask()

            if habit_three:
                habit_name = "Drinking 2 liters of water"
                description = "Drinking at least two liters of water every day"
                category = "nutrition"
                frequency = "daily"
                new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
                new_habit.store(db)
            else:
                pass

            habit_four = questionary.confirm("Habit: Morning Yoga | Frequency: Daily. Do you want to add this habit?"
                                             ).ask()

            if habit_four:
                habit_name = "Morning Yoga"
                description = "Start the day with ten rounds of of Surya Namaskar"
                category = "sport"
                frequency = "daily"
                new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
                new_habit.store(db)
            else:
                pass

            habit_five = questionary.confirm("Habit: Practicing Spanish | Frequency: Daily. "
                                             "Do you want to add this habit?"
                                             ).ask()

            if habit_five:
                habit_name = "Practicing spanish"
                description = "Learn twenty new spanish words"
                category = "education"
                frequency = "weekly"
                new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
                new_habit.store(db)
            else:
                pass

        if len(habit_list) != 0:
            pass

    def habit_creation(self):
        """
        A function used to create and store a new habit. The user has to enter a habit name, a description, select a
        category and the frequency at which he/she has to complete the habit
        """
        db = get_db()

        def habit_validation():
            """
            A function used to validate the chosen habit name. Two users can have a habit with the same name,
            but for each user, every habit name must be individual.
            :return: the name of the new habit
            """
            while True:
                new_habit_name = questionary.text("Please enter a habit name:").ask()
                habit_name_validation = get_habit_data(db, new_habit_name, self[0][2])
                if habit_name_validation:
                    print("Habit already exists, please choose different name")
                else:
                    print("Habit name is valid.")
                    break
            return new_habit_name

        with db:
            user_email = self[0][2]
            habit_name = habit_validation()
            creation_date = str(date.today())
            description = questionary.text("Please add a description to the habit:").ask()
            category = questionary.select(
                "Which category does your habit belong to?",
                choices=[
                    'sport',
                    'well being',
                    'nutrition',
                    'education',
                    'creativity'
                ],
            ).ask()
            frequency = questionary.select(
                "Please choose the frequency:",
                choices=[
                    'daily',
                    'weekly'
                ],
            ).ask()

            new_habit = HabitClass(habit_name, description, category, frequency, user_email, creation_date)
            new_habit.store(db)

    def habit_management(self):
        """
        A function used to manage previously created habits. A user can either delete a habit or edit the name,
        description, category or frequency of a habit. The database entry in the table habits is then either deleted or
        overwritten.
        :return:
        """
        db = get_db()
        user_email = self[0][2]
        management_question = questionary.select(
            "Do you want to edit or delete a habit?",
            choices=[
                'edit',
                'delete'
            ],
        ).ask()

        if management_question == "edit":
            cur = db.cursor()
            habit_list = []
            cur.execute("SELECT habit_name FROM habits WHERE user_email=?", (user_email,))
            records = cur.fetchall()
            for row in records:
                habit_list.append(row[0])

            choices = habit_list

            habit_name_edit = questionary.select("Please choose the habit you want to edit:",
                                                 choices=choices).ask()

            element_edit = questionary.select("Which element do you want to edit?",
                                              choices=[
                                                  'habit name',
                                                  'description',
                                                  'category',
                                                  'frequency'
                                              ]).ask()

            if element_edit == "habit name":
                habit_name_update = questionary.text("Please enter a new habit name:").ask()

                # habit name is being overwritten in the database table habits
                statement = f"UPDATE habits SET habit_name = '{habit_name_update}' " \
                            f"WHERE habit_name='{habit_name_edit}' AND user_email= '{user_email}';"
                cur.execute(statement)
                db.commit()
                print("The habit " + habit_name_edit + ' has been changed to ' + habit_name_update + '!')

            if element_edit == "description":
                description_update = questionary.text("Please enter a new description:").ask()

                # description is being overwritten in the database table habits
                statement = f"UPDATE habits SET description = '{description_update}' " \
                            f"WHERE habit_name='{habit_name_edit}' AND user_email= '{user_email}';"
                cur.execute(statement)
                db.commit()
                print("The description has been updated.")

            if element_edit == "category":
                category_update = questionary.select("Which category does your habit belong to?",
                                                     choices=[
                                                         'sport',
                                                         'well being',
                                                         'nutrition'
                                                     ],
                                                     ).ask()

                # category is being overwritten in the database table habits
                statement = f"UPDATE habits SET category = '{category_update}' " \
                            f"WHERE habit_name='{habit_name_edit}' AND user_email= '{user_email}';"
                cur.execute(statement)
                db.commit()
                print("The category has been updated.")

            if element_edit == "frequency":
                frequency_update = questionary.select("Please choose the frequency:",
                                                      choices=[
                                                          'daily',
                                                          'weekly'
                                                      ],
                                                      ).ask()

                # preiodicity is being overwritten in the database table habits
                statement = f"UPDATE habits SET frequency= '{frequency_update}' " \
                            f"WHERE habit_name='{habit_name_edit}' AND user_email= '{user_email}';"
                cur.execute(statement)
                db.commit()
                print("The frequency has been updated.")

        if management_question == "delete":
            cur = db.cursor()
            habit_list = []
            cur.execute("SELECT habit_name FROM habits WHERE user_email=?", (user_email,))
            records = cur.fetchall()
            for row in records:
                habit_list.append(row[0])

            choices = habit_list

            habit_name_edit = questionary.select("Please choose the habit you want to delete:",
                                                 choices=choices).ask()

            validation = questionary.select("Are you sure, you want to delete the habit?",
                                            choices=[
                                                'yes',
                                                'no']
                                            ).ask()

            if validation == "yes":
                # the row with the selected habit name is being deleted from the database table habits as well as all
                # corresponding entries in the database table habits_analysis
                statement = f"DELETE FROM habits WHERE habit_name='{habit_name_edit}' AND user_email= '{user_email}';"
                cur.execute(statement)
                statement = f"DELETE FROM habits_analysis WHERE habit_name='{habit_name_edit}' " \
                            f"AND user_email= '{user_email}';"
                cur.execute(statement)
                db.commit()
                print("The habit " + habit_name_edit + " has been deleted.")
