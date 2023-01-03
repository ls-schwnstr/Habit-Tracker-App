# Habit-Tracker-App

## Installation

### Requirements
To run successfully, the application requires the following programs and modules:
1. Python 3.7+
2. An IDE such as PyCharm
3. The modules questionary, freezegun, pytest

### Installation steps
1. Install the latest version of Python on your computer
2. Open all files with the IDE of your choice and install the required modules
3. Run main.py

## Functionalities

#### Registration

- A user can register by entering his first name, last name, email-address and a chosen password
- If the email-address is already registered, the user has to choose a different email-address
- If the password has a length of at least 5 letters, the user profile is created 

#### Login
- The user has to log in with his email-address and password

#### Habit Creation
- If the user has no habits yet, he can choose from five predefined habits
- Additionally, the user can create habits via selecting "create" in the main overview 
- To create a habit, the user has to pick a name, description, category and periodicity

#### Habit Tick-Off
- Every time the user log in, the app lists all habits that can currently be ticked off. 
- The user has to specify whether he has completed the habit yet or not
- Additionally, every time after a new habit has been created, the app asks the user whether he has completed the current habits

#### Habit Management
- Habits can be deleted or edited via selecting "manage" in the main overview

#### Habit Analyzation
- Habits can be analyzed in the analytics overview by selecting "analyze" in the main overview

##### show habits with same periodicity
- The user can choose for which periodicity he wants to see his habits
- all habits belonging to the user are listed based on the chosen periodicity

##### show longest streak for a habit
- for each habit belonging to the user the longest streak is listed

##### show longest streak in total
- the habit with the longest streak in total is listed with the associated streak

##### show current streak for each habit
- for each habit, the current streak is listed

##### show all currently tracked habits
- all habits belonging to the user are listed


## Testing
The code comes with a testing file testdata.py including testdata and different tests for computing streaks and analyzing habits. 
Additionally, the database main.py can be used for further testing.  
