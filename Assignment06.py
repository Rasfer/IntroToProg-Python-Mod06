# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   REidswick, 11/17/2025, Modified script with functions
# ------------------------------------------------------------------------------------------ #

import json
import sys
import traceback

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
students: list = []  # a table of student data
menu_choice: str = ''  # Hold the choice made by the user.

# Classes
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    REidswick, 11/18/2025, Created Class
    REidswick, 11/18/2025, Added functions for read/write of a file
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ Function that reads data from json files

        :param file_name: name of the json file
        :param student_data: empty list
        :return: student first name, student last name, and course name from json file
        """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
        except FileNotFoundError as e:
            IO.output_error_message("File must be created first. Creating the file...", e)
            file = open(file_name, "w")
            json.dump(student_data, file, indent=4)
        except Exception as e:
            IO.output_error_message("There was a non-specific error when reading the file.", e)
            pass
        finally:
            if file is not None:
                file.close()

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ Function that writes data from json files

        :param file_name: name of the json file
        :param student_data: list of student first name, last name, and course
        :return: None
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=4)
        except TypeError as e:
            IO.output_error_message("There was a TypeError exception while writing data to file",e)
        except Exception as e:
            IO.output_error_message("There was a non-specific exception while writing data to file",e)
        finally:
            if file is not None:
                file.close()

class IO:
    """
    A  collection of presentation layer functions that manage user
    input and output

    ChangeLog: (Who, When, What)
    REidswick, 11.18.2025, Created Class
    REidswick, 11.18.2025, Added menu output and input functions
    REidswick, 11.18.2025, Added a function to display the data
    REidswick, 11.18.2025, Added a function to display custom error messages
    """
    @staticmethod
    def output_error_message(message: str, error: Exception = None):
        """ Creates an error message to handle exceptions.

        :param message: message to display to the user
        :param error: Exception type
        :return: None
        """
        print("="*50)
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """Print menu for user to see

        :param menu: menu to print
        :return: None
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """ Function that prompts the user to select from the menu.

        :return: menu choice
        """
        choice = "0"
        try:
            choice = input("Please select from 1,2,3, or 4: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please select from 1,2,3, or 4")
        except Exception as e:
            IO.output_error_message(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ Function that prints student courses

        :param student_data: list of student first name, last name, and course
        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ Function that adds new student data to the list.

        :param student_data: current student data
        :return: updated student data
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            new_student_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            student_data.append(new_student_data)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_message("There was a ValueError exception while reading the data.", e)
        except Exception as e:
            IO.output_error_message("There was a ValueError exception while reading the data.", e)
        return student_data


# Main
students = FileProcessor.read_data_from_file(FILE_NAME, students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
