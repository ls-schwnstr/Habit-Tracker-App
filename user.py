from db import get_db, get_user_data, add_user
import questionary


class UserClass:
    """
    A class used to represent the user accounts.
    """

    def __init__(self, firstname: str, lastname: str, email: str, password: str):
        """
        :param firstname: the user's first name
        :param lastname: the user's last name
        :param email: the user's email-address
        :param password: the user's password
        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

        self.db = get_db()
        self.cur = self.db.cursor()

    def store(self, db):
        """
        A function used to store the user's data
        :param db: connection object
        """
        add_user(db, self.firstname, self.lastname, self.email, self.password)

    def __str__(self):
        """
        A function used to represent the class objects as a string
        :return: string of the class object
        """
        return f"{self.firstname} {self.lastname} {self.email} {self.password}"

    def __getitem__(self, email):
        """
        A function used for accessing the list item user_email
        :param email: the email-address of the current user
        :return: user_email
        """
        return self.email


def registration():
    """
    A function used to create a new account where the user enters firstname, last name, email-address and password.
    """
    db = get_db()
    cur = db.cursor()

    def pw_validation():
        """
        A function used to create the user's password. The user has to enter a password with at least five letters.
        :return: the user's new password
        """
        while True:
            new_password = str(input("Please enter a password: "))
            if len(new_password) < 5:
                print("Please choose a password with at least 5 letters!")
            else:
                print("Your password is strong enough.")
                break
        return new_password

    def pw_confirmation():
        """
        A function used to validate the user's password. The user has to reenter the password he has chosen in the
        previous step.
        :return: the validation process is finished once the user has entered the pre chosen password.
        """
        while True:
            password_confirmation = questionary.text("Please repeat your password: ").ask()
            if password_confirmation == password:
                print("Your account has been created. Please login now.")
                break
            else:
                print("the passwords don't match, please try again")
        return True

    def email_registration():
        """
        A function used to create a new account with an email-address. The email-address must not yet be registered.
        :return: the user's email-address
        """
        while True:
            new_email = questionary.text("Please enter your email address:").ask()
            if cur.execute('SELECT * FROM users WHERE email = ?', (new_email,)):
                if cur.fetchone():
                    print("email-address is already registered, please choose a different email-address ")
                else:
                    print("email-address is valid")
                    break
        return new_email

    with db:
        firstname = questionary.text("Please enter your first name: ").ask()
        lastname = questionary.text("Please enter your last name: ").ask()
        email = email_registration()
        password = pw_validation()
        new_user = UserClass(firstname, lastname, email, password)
        pw_confirmation()
        new_user.store(db)


def login():
    """
    A function used to log in. The user has to enter the email-address and password he/she has chosen during
    registration.
    :return: the current user
    """
    while True:
        db = get_db()
        cur = db.cursor()
        login_email = questionary.text("Please enter your email address: ").ask()
        user = get_user_data(db, login_email)
        if user:
            login_password = questionary.text("Please enter your password: ").ask()
            statement = f"SELECT email FROM users WHERE email='{login_email}' AND password= '{login_password}';"
            cur.execute(statement)
            if not cur.fetchone():
                print("Wrong password, please try again")
            else:
                print("Welcome!")
                break
        else:
            print("Invalid email-address.")
    return user
