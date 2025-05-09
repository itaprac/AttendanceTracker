import csv
import os
import platform
from typing import List

from tinydb import TinyDB

from course import Course


class CourseTracker:
    def __init__(self) -> None:
        self.courses: List[Course] = []
        self.create_database()

    def add_course(self, name: str, format: str, un_classes: int = 0) -> None:
        for course in self.courses:
            if course.name == name and course.format == format:
                raise ValueError("Ten kurs juz istnieje")
        self.courses.append(Course(name, format, un_classes))
        self.save_courses()

    def remove_course(self, name: str, format: str) -> None:
        for course in self.courses:
            if course.name == name and course.format == format:
                self.courses.remove(course)
        self.save_courses()

    def reset_data(self) -> None:
        self.courses = []
        self.save_courses()

    # Type cheking for tinydb??
    def get_course(self, name: str, format: str):
        for course in self.courses:
            if course.name == name and course.format == format:
                return course
        raise ValueError("Ten kurs nie istnieje")

    def list_courses(self) -> List[Course]:
        return sorted(self.courses, key=lambda x: (x.name, x.format))

    def list_courses_str(self) -> list[str]:
        return [str(course) for course in self.courses]

    def increment_unattended(self, name: str, format: str) -> None:
        course = self.get_course(name, format)
        course.increment_un_classes()
        self.save_courses()

    def decrement_unattended(self, name: str, format: str) -> None:
        course = self.get_course(name, format)
        course.decrement_un_classes()
        self.save_courses()

    def create_database(self) -> None:
        # directory = "."
        if platform.system() == "Darwin":  # macOS
            directory = os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Application Support",
                "CourseAttendanceTracker",
            )
        elif platform.system() == "Windows":
            appdata_path = os.getenv("APPDATA")
            if appdata_path is None:
                raise ValueError("APPDATA environment variable is not set")

            directory = os.path.join(appdata_path, "CourseAttendanceTracker")
        else:  # Linux and other OS
            directory = os.path.join(
                os.path.expanduser("~"), ".CourseAttendanceTracker"
            )

        if not os.path.exists(directory):
            os.makedirs(directory)
        self.database = os.path.join(directory, "course_databse.json")
        self.db = TinyDB(self.database)
        self.load_courses()

    def save_courses(self) -> None:
        self.db.truncate()
        for course in sorted(self.courses, key=lambda x: (x.name, x.format)):
            self.db.insert(
                {
                    "name": course.name,
                    "format": course.format,
                    "un_classes": course.un_classes,
                }
            )

    def load_courses(self):
        self.courses = []
        if not os.path.exists(self.database):
            print(f"File {self.database} does not exist. Returning empty list")
            return

        try:
            self.db = TinyDB(self.database)
            for course in self.db.all():
                self.courses.append(
                    Course(course["name"], course["format"], course["un_classes"])
                )
        except Exception as e:
            print(f"Error loading courses: {e}")

    def export_courses(self, filename: str, test, test2, test3, test4, test5, test6, test7,) -> None:
        fields = ["Nazwa", "Format", "Opuszczone"]
        rows = [
            [course.name, course.format, str(course.un_classes)]
            for course in self.courses
        ]

        with open(filename, "w", newline="") as csvfile:
            csv.writer(csvfile).writerows([fields] + rows)

    def import_courses_replace(self, filename: str) -> None:
        self._import_courses(filename, replace=True)

    def import_courses_append(self, filename: str) -> None:
        self._import_courses(filename, replace=False)

    def _import_courses(self, filename: str, replace: bool) -> None:
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            return

        try:
            with open(filename, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                new_courses = [Course(row[0], row[1], int(row[2])) for row in reader]

            if replace:
                self.courses = new_courses
            else:
                for course in new_courses:
                    if course not in self.courses:
                        self.courses.append(course)
                    else:
                        print(f"Course {course.name}, {course.format} already exists")

            self.save_courses()
        except (csv.Error, Exception) as e:
            print(f"Error importing courses from {filename}: {str(e)}")
