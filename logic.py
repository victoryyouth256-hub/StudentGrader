import csv
from PyQt6.QtWidgets import *
from gui import *


class Person:
    def __init__(self, name: str) -> None:
        """Stores the name of a person."""
        self.__name = name.strip()

    def get_name(self) -> str:
        """Returns the name."""
        return self.__name

    def __str__(self) -> str:
        """Returns the name as a string."""
        return self.__name


class Student(Person):
    def __init__(self, name: str, score: int) -> None:
        """Creates a student with a name and a score."""
        super().__init__(name)
        if score < 0 or score > 100:
            raise ValueError('Score must be between 0 and 100')
        self.__score = score
        self.__grade = ''

    def get_score(self) -> int:
        """Returns the score."""
        return self.__score

    def get_grade(self) -> str:
        """Returns the letter grade."""
        return self.__grade

    def set_grade(self, grade: str) -> None:
        """Sets the letter grade."""
        self.__grade = grade

    def __str__(self) -> str:
        """Returns the student as text for the list."""
        if self.__grade == '':
            return f'{self.get_name()} - score {self.__score}'
        return f'{self.get_name()} - score {self.__score} - grade {self.__grade}'


class Gradebook:
    def __init__(self) -> None:
        """Creates an empty list of students."""
        self.__students = []

    def add_student(self, student: Student) -> None:
        """Adds a student to the list."""
        self.__students.append(student)

    def get_students(self) -> list:
        """Returns the list of students."""
        return self.__students

    def count(self) -> int:
        """Returns how many students are in the list."""
        return len(self.__students)

    def clear(self) -> None:
        """Removes all students."""
        self.__students = []

    def get_best_score(self) -> int:
        """Returns the highest score in the list."""
        scores = []
        for student in self.__students:
            scores.append(student.get_score())
        return max(scores)

    def get_grade(self, score: int, best: int) -> str:
        """Returns the grade for a score based on the best score."""
        if score >= best - 10:
            return 'A'
        elif score >= best - 20:
            return 'B'
        elif score >= best - 30:
            return 'C'
        elif score >= best - 40:
            return 'D'
        else:
            return 'F'

    def assign_grades(self) -> int:
        """Gives every student a grade and returns the best score."""
        best = self.get_best_score()
        for student in self.__students:
            student.set_grade(self.get_grade(student.get_score(), best))
        return best


class GradeStorage:
    def __init__(self, file_name: str) -> None:
        """Stores the name of the csv file."""
        self.__file_name = file_name

    def get_file_name(self) -> str:
        """Returns the csv file name."""
        return self.__file_name

    def save_students(self, students: list) -> None:
        """Appends each student's name, score and grade to the csv file."""
        try:
            with open(self.__file_name, 'r') as csv_file:
                has_header = csv_file.readline() != ''
        except:
            has_header = False

        with open(self.__file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not has_header:
                writer.writerow(['Name', 'Score', 'Grade'])
            for student in students:
                writer.writerow([student.get_name(), student.get_score(), student.get_grade()])


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """Sets up the window and connects the buttons."""
        super().__init__()
        self.setupUi(self)

        self.__gradebook = Gradebook()
        self.__storage = GradeStorage('grades.csv')

        self.button_add.clicked.connect(lambda: self.add_student())
        self.button_grade.clicked.connect(lambda: self.calculate_grades())
        self.button_clear.clicked.connect(lambda: self.clear_all())

    def add_student(self) -> None:
        """Checks the name and score entered, then adds the student to the list."""
        name = self.input_name.text().strip()
        if name == '':
            self.label_message.setText('Please enter a student name')
            return
        if not name.replace(' ', '').isalpha():
            self.label_message.setText('Name must only contain letters')
            self.input_name.clear()
            return

        try:
            score = int(self.input_score.text().strip())
            student = Student(name, score)
        except ValueError:
            self.label_message.setText('Score must be a whole number between 0 and 100')
            self.input_score.clear()
        else:
            self.__gradebook.add_student(student)
            self.list_students.addItem(str(student))
            self.label_message.setText(f'Added {name}. Total students: {self.__gradebook.count()}')
            self.input_name.clear()
            self.input_score.clear()
            self.input_name.setFocus()

    def calculate_grades(self) -> None:
        """Assigns grades based on the best score and saves them to the csv file."""
        if self.__gradebook.count() == 0:
            self.label_message.setText('Add at least one student first')
            return

        best = self.__gradebook.assign_grades()
        self.label_best.setText(f'Best score: {best}')

        self.list_students.clear()
        for student in self.__gradebook.get_students():
            self.list_students.addItem(str(student))

        try:
            self.__storage.save_students(self.__gradebook.get_students())
        except:
            self.label_message.setText('Grades calculated but the file could not be saved')
        else:
            self.label_message.setText(f'Grades saved to {self.__storage.get_file_name()}')

    def clear_all(self) -> None:
        """Clears the list and resets the window."""
        self.__gradebook.clear()
        self.list_students.clear()
        self.label_best.setText('Best score: --')
        self.input_name.clear()
        self.input_score.clear()
        self.label_message.setText('Please enter a student name and score')
        self.input_name.setFocus()
