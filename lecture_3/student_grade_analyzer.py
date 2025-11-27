"""
Student Grade Analyzer Application — a lightweight student grade
management tool

Provide a command-line interface for managing student grade records.
Users can add students, input their grades, generate reports, and
identify the top performer.
"""

from __future__ import annotations

from typing import TypedDict


class Student(TypedDict):
    name: str
    grades: list[int]


def find_student(
    lookup: dict[str, Student], student_name: str
) -> Student | None:
    """
    Search for and retrieve a student by name in the students' lookup.

    Lookup dictionary collection and return student's dictionary
    that matches the name.

    Params:
        lookup (dict[str, Student]): A dictionary map for
                                corresponding students' dictionaries.
        name (str): The name of the student to search for.
    Returns:
        Student | None: A dictionary with student
                            data or None if the student is not found.
    """
    return lookup.get(student_name)


def any_grades(students: list[Student]) -> bool:
    """
    Check whether any grades exist in the records.
    If no grades exist, display an informative message.

    Params:
        students (list[Student]): A list of dictionaries
                                        with student data.
    Returns:
        bool: True if any grades exist, otherwise False.
    """
    if not any(student["grades"] for student in students):
        print("\n    No grades are present in the records yet.")
        return False
    return True


def calculate_average(grades: list[int | float]) -> float:
    """
    Calculate the average of grades.

    Params:
        grades (list[int]): A list of grades as integers.
    Returns:
        float: The average of the grades as a float
                rounded to one decimal place.
    """
    return round(sum(grades) / len(grades), 1)


def check_name() -> str | None:
    """
    Prompt user to input a student name, validate the input,
    and return a formatted name.

    Enforce that the input name is non-empty, consists only of
    alphabetic characters, spaces, dashes and apostrophes and
    trim unnecessary whitespace. User can enter '1' to return
    to the main menu.

    Returns:
            str | None: Formatted student name if valid
            or None if '1' keyword is entered.
    """
    allowed_char = " -‐‑–'ʼ'′"

    while True:
        name_input = input(
            "    Enter student name (or '1' to return to main menu): "
        ).strip()

        if not name_input:
            print("    Name cannot be empty.")
            continue

        # Return to main menu:
        if name_input == "1":
            return None

        # Enforce name contains only alphabetic characters, spaces,
        # dashes and apostrophes:
        if not all(
            char.isalpha() or char in allowed_char for char in name_input
        ):
            print("    Please enter a valid name.")
            continue

        # Format name with proper capitalization and spacing:
        return " ".join(name_input.split()).title()


def add_student(students: list[Student], lookup: dict[str, Student]) -> None:
    """
    Add a new student to the students' data list.
    If the student already exists, display an informative message.

    Params:
        students (list[Student]): A list of dictionaries
                                        with student data.
        lookup (dict[str, Student]): A dictionary map for
                                corresponding students' dictionaries.
    Returns: None.
    """
    # If user pressed 1 and returned to the main menu:
    if not (student_name := check_name()):
        return

    if find_student(lookup, student_name):
        print(f"\n    Student '{student_name}' already exists.")
        return

    student: Student = {"name": student_name, "grades": []}
    # Add dictionary to the students' data list:
    students.append(student)

    # Add dictionary to the lookup table:
    lookup[student_name] = student
    print(f"\n    Student '{student_name}' added successfully.")


def add_grades(students: list[Student], lookup: dict[str, Student]) -> None:
    """
    Add grades to an existing student record.

    Allow user to input grades for a specific student. Enforce
    that the grades are integers and within the range of 0 to 100.
    If no students are present in the records, or if a
    specified student cannot be found, display an informative
    message. User can enter 'done' to stop adding grades.

    Display informative messages for invalid inputs as well.

    Params:
        students (list[Student]): A list of dictionaries
                                        with student data.
        lookup (dict[str, Student]): A dictionary map for
                                corresponding students' dictionaries.
    Returns: None.
    """
    if not students:
        print("\n    No students are present in the records yet.")
        return

    # Unreachable: kept to satisfy type checker:
    if not (student_name := check_name()):
        return

    if not (student := find_student(lookup, student_name)):
        print("\n    Student not found.")
        return

    while True:
        grade_input = input("    Enter a grade (or 'done' to finish): ")
        if grade_input.lower() == "done":
            break
        try:
            grade = int(grade_input)
        except ValueError:
            print(
                "    Invalid input. Please enter a number between 0 and 100."
            )
            continue
        if 0 <= grade <= 100:
            student["grades"].append(grade)
            print(f"    Grade '{grade}' added.")
        else:
            print(
                "    Invalid grade. Please enter a number between 0 and 100."
            )


def generate_report(students: list[Student]) -> None:
    """
    Generate and print comprehensive grade report for all students.

    The report includes individual student averages, the maximum
    average, the minimum average, and the overall average grade.

    If no students are present in the records, or if no grades are
    available for any student, print an informative message instead.

    Params:
        students (list[Student]): A list of dictionaries
                                        with student data.
    Returns: None.
    """
    if not students:
        print("\n    No students are present in the records yet.")
        return

    # Check if any grades in the students' dictionary:
    if any_grades(students):

        print("\n    --- Report ---")
        all_averages: list[float] = []
        for student in students:
            try:
                # Count average for each student and add it to list:
                average: float = calculate_average(student["grades"])
                all_averages.append(average)
                print(f"    {student['name']}'s average grade is {average}.")
            except ZeroDivisionError:
                print(f"    {student['name']}'s average grade is N/A.")

        overall_average: float = calculate_average(all_averages)
        print(
            f"    --------------------------\n"
            f"    Max Average: {max(all_averages)}\n"
            f"    Min Average: {min(all_averages)}\n"
            f"    Overall Average: {overall_average}"
        )


def top_performer(students: list[Student]) -> None:
    """
    Identify and display student(s) with the highest average grade.

    If no students are present in the records, or if no grades are
    available for any student, print an informative message instead.

    Params:
        students (list[Student]): A list of dictionaries
                                        with student data.
    Returns: None.
    """
    if not students:
        print("\n    No students are present in the records yet.")
        return

    if any_grades(students):

        # Calculate and collect in a list the averages paired with
        # their corresponding names for all students who have grades:
        all_averages: list[tuple[str, float]] = [
            (student["name"], calculate_average(student["grades"]))
            for student in students
            if student["grades"]
        ]
        # Define student with the highest average grade,
        # -1 removes students without grades:
        top_student: Student = max(
            students,
            key=lambda student: (
                calculate_average(
                    student["grades"] if student["grades"] else [-1]
                )
            ),
        )

        top_average: float = calculate_average(top_student["grades"])
        # Find all students with the maximum average:
        all_top_students: list[str] = [
            name for name, average in all_averages if average == top_average
        ]

        # Print option for a single top student:
        if len(all_top_students) == 1:
            print(
                f"\n    The student with the highest average is "
                f"{all_top_students[0]} with a grade of "
                f"'{top_average}'."
            )
        else:

            # Creat a string for multiple top students:
            names_of_tops: str = (
                ", ".join(all_top_students[:-1])
                + f" and {all_top_students[-1]}"
            )
            print(
                f"\n    The students with the highest average grade "
                f"of '{top_average}' are: {names_of_tops}"
            )


def main() -> None:
    """
    Provide an interface for Student Grade Analyzer application.

    Act as the entry point and the driver for the program,
    displaying a menu and giving options for students' management
    tasks: adding students and their grades, generating reports and
    representing the top performer.

    Contain variables with student data.

    Check for valid input and gracefully handle ValueError.

    Returns: None.
    """
    # Student data collection:
    students: list[Student] = []

    # A hash-table lookup for students' records:
    lookup: dict[str, Student] = {}

    while True:
        get_choice = input(
            """\n    --- Student Grade Analyzer ---
    1. Add a new student
    2. Add grades for a student
    3. Generate a full report
    4. Find the top student
    5. Exit program
    Enter your choice: """
        )
        try:
            choice = int(get_choice)
        except ValueError:
            print("\n    Please enter a valid option.")
            continue

        match choice:
            case 1:
                add_student(students, lookup)
            case 2:
                add_grades(students, lookup)
            case 3:
                generate_report(students)
            case 4:
                top_performer(students)
            case 5:
                print("\n    Exiting program...")
                break
            case _:
                print("\n    Please enter a valid option.")


if __name__ == "__main__":
    main()
