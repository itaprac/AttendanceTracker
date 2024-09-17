from course import Course
import pickle
import os
import csv


class CourseTracker:
    def __init__(self, filename: str = "courses.pkl"):
        self.filename = filename
        self.courses: list[Course] = self.load_courses()

    def add_course(self, name: str, format: str) -> None:
        for course in self.courses:
            if course.name == name and course.format == format:
                raise ValueError("This course already exists")
        self.courses.append(Course(name, format))
        self.save_courses()

    def remove_course(self, name: str, format: str) -> None:
        # self.courses = [
        #     c for c in self.courses if not (c.name == name and c.format == format)
        # ]
        for course in self.courses:
            if course.name == name and course.format == format:
                self.courses.remove(course)
        self.save_courses()

    def reset_data(self) -> None:
        self.courses = []
        self.save_courses()

    def get_course(self, name: str, format: str) -> Course:
        for course in self.courses:
            if course.name == name and course.format == format:
                return course
        raise ValueError("This course doesn't exist")

    def list_courses(self) -> list[Course]:
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

    def save_courses(self) -> None:
        with open(self.filename, "wb") as f:
            pickle.dump(self.courses, f)

    def load_courses(self) -> list[Course]:
        if not os.path.exists(self.filename):
            print(f"File {self.filename} does not exist. Returning an empty list.")
            return []

        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, Exception) as e:
            print(f"Error loading {self.filename}: {str(e)}. Returning an empty list.")
            return []

    def export_courses(self, filename: str) -> None:
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
