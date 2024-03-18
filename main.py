import sqlite3
import pyfiglet
import termcolor
import datetime
import os


# Function to clear the terminal screen
def clear_screen():
    return os.system("clear")


# Clear the screen
clear_screen()

# Welcome message
print(termcolor.colored(pyfiglet.figlet_format("TO DO"), color="yellow"))
print(termcolor.colored("*" * 50, color="red"), end="\n")
print(termcolor.colored("Design By: ", color="red"), end=" ")
print(termcolor.colored("Mano", color="white"))
print(termcolor.colored("Version: ", color="red"), end=" ")
print(termcolor.colored("1.0.0", color="white"))
print(termcolor.colored("*" * 50, color="red"))

# Introductory message
string = "Welcome to do list script.."
print(termcolor.colored(string, color="blue"), end="\n")
print(termcolor.colored("*" * 50, color="red"))

# Create database connection
db = sqlite3.connect("app.db")
cr = db.cursor()

# Create the ToDo table if it doesn't exist
cr.execute(
    "CREATE TABLE if not exists ToDo(user_id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed BOOLEAN, due_date TEXT)"
)


def main():
    """
    Main function to display menu options and handle user choices.

    Menu:
    1 - Add Task
    2 - Mark Task
    3 - View Task
    4-  Edit Task
    5 - Quit
    """

    while True:
        print(termcolor.colored(main.__doc__, color="grey"))
        try:
            choice = int(
                input(termcolor.colored("Enter Your Choice: ", color="blue")).strip()
            )

            if choice == 1:
                add_task()
            elif choice == 2:
                mark_task()
            elif choice == 3:
                view_task()
            elif choice == 4:
                edit_task()
            elif choice == 5:
                print(termcolor.colored("Nice To See You!", color="black"))
                break
        except ValueError:
            print(termcolor.colored("Invalid Choice!", color="red"))


def add_task():
    """
    Function to add a task to the ToDo list.

    Prompts the user for a task name, generates a unique user_id,
    checks if the task already exists, and inserts the task into the database.
    """

    task = (
        input(termcolor.colored("Enter Your Task: ", color="blue")).strip().capitalize()
    )

    # Get the current date
    current_date = datetime.datetime.now().strftime("%a, %d %B %Y")

    # Generate a unique user_id based on current second
    user_id = datetime.datetime.now().second

    # Check if the task already exists and delete it
    cr.execute(f"SELECT * FROM ToDo")
    result = cr.fetchall()
    for row in result:
      if task == any(row[1]):
        cr.execute(f"DELETE FROM ToDo WHERE task = '{row[1]}'")

    # Insert the new task into the database
    cr.execute(
        f"INSERT INTO ToDo(user_id, task, completed, due_date) VALUES ({user_id}, '{task}', False, '{current_date}')"
    )

    db.commit()
    print(termcolor.colored("Task added successfully!", color="grey"))


def mark_task():
    """
    Function to mark a task as completed.

    Displays the list of tasks, prompts the user for the task ID,
    and updates the task's 'completed' status in the database.
    """

    # Show tasks to the user
    cr.execute("SELECT * FROM ToDo")
    results = cr.fetchall()

    # Check if there are tasks
    if not results:
        print(termcolor.colored("No Tasks To Mark as complete!", color="red"))
        return

    for row in results:
        print(
            termcolor.colored(row[0], color="white")
            + ":"
            + termcolor.colored(row[1], color="blue")
            + ":"
            + termcolor.colored(row[3], color="white")
        )
        print("*" * 50)

    try:
        task_id = int(
            input(
                termcolor.colored(
                    "Enter task number to mark as complete: ", color="white"
                )
            ).strip()
        )

        # Update the task's 'completed' status
        cr.execute(
            f"UPDATE ToDo SET completed = True WHERE user_id = {task_id}"
        )
        db.commit()
        print(termcolor.colored("Marked Completed Successfully!", color="green"))

    except (sqlite3.Error, ValueError) as err:
        print(
            termcolor.colored("Invalid Value, Enter a valid task number!", color="red")
        )


def view_task():
    """
    Function to view tasks in the ToDo list.

    Displays all tasks in the database along with their completion status.
    """

    cr.execute("SELECT * FROM ToDo")
    results = cr.fetchall()

    # Check if there are tasks
    if not results:
        print(termcolor.colored("No Tasks To Display!", color="red"))
        return

    for row in results:
        print(termcolor.colored(row[0], color="white"), end=": ")

        if row[2] == True:
            print(termcolor.colored(row[1], color="green"), end=": ")

        else:
            print(termcolor.colored(row[1], color="red"), end=": ")

        print(termcolor.colored(row[3], color="white"))

        print(termcolor.colored("*" * 50, color="yellow"))


def edit_task():
    """
    Function to edit an existing task.

    Prompts the user for the task ID and new task details,
    and updates the task in the database.
    """

    cr.execute("SELECT * FROM ToDo")
    results = cr.fetchall()

    if not results:
        print(termcolor.colored("No Task to Edit!"))
        return

    for row in results:
        print(
            termcolor.colored(row[0], color="white")
            + ":"
            + termcolor.colored(row[1], color="blue")
        )
        print("*" * 50)

    try:
        task_id = int(
            input(termcolor.colored("Enter task id to edit: ", color="red")).strip()
        )

        new_task = (
            input(termcolor.colored("Enter new task: ", color="green"))
            .strip()
            .capitalize()
        )

        cr.execute(f"UPDATE ToDo SET task = '{new_task}' WHERE user_id = {task_id}")
        db.commit()
        print(termcolor.colored("Task Edit Successfuly!",color="grey"))

    except (sqlite3.Error, ValueError):
        print("Invalid Number")


if __name__ == "__main__":
    main()

# Close the database connection
db.close()
