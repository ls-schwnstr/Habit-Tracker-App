import questionary

from db import get_tickable_habits_list, get_db
from user import login, registration
from habit import HabitClass
from Analytics import habit_analysis, habit_progress_confirmation


def login_page():
    """
    A function used to run the login and registration process.
    :return: the credentials of the active user
    """

    while True:
        login_interface = questionary.select(
            "Do you want to register or login?",
            choices=[
                'login',
                'register',
            ],
        ).ask()

        if login_interface == "register":
            registration()
            current_user = login()
            break
        elif login_interface == "login":
            current_user = login()
            break
    return current_user


def main_page():
    """
    A function used to run the main page where the user can create, manage or analyze habits.
    """
    db = get_db()
    current_user = login_page()
    HabitClass.add_predefined_habit(current_user)
    habit_tick_off_list = get_tickable_habits_list(db, current_user)
    habit_progress_confirmation(db, current_user, habit_tick_off_list)

    while True:
        menu_question = questionary.select(
            "Do you want to create, manage or analyze a habit?",
            choices=[
                'create',
                'manage',
                'analyze',
                'exit',
            ],
        ).ask()

        if menu_question == "create":
            HabitClass.habit_creation(current_user)
            habit_tick_off_list = get_tickable_habits_list(db, current_user)
            habit_progress_confirmation(db, current_user, habit_tick_off_list)

        if menu_question == "manage":
            HabitClass.habit_management(current_user)

        if menu_question == "analyze":
            habit_analysis(current_user)
        if menu_question == "exit":
            print("goodbye!")
            break
    return True


if __name__ == '__main__':
    main_page()
