from course import Course
import pickle
import os


class CourseTracker:
    """
    A class to track courses and their unattended classes.

    Attributes:
        filename (str): The name of the file where courses are saved.
        courses (list[Course]): A list of courses being tracked.
    """

    def __init__(self, filename: str = "courses.pkl"):
        """
        Initializes the CourseTracker with an optional filename for saving/loading courses.

        Args:
            filename (str): The name of the file where courses are saved. Defaults to "courses.pkl".
        """
        self.filename = filename
        self.courses: list[Course] = self.load_courses()

    def add_course(self, name: str, format: str) -> None:
        """
        Adds a new course to the tracker.

        Args:
            name (str): The name of the course.
            format (str): The format of the course (e.g., Online, Offline).
        """
        for course in self.courses:
            if course.name == name and course.format == format:
                raise ValueError("This course already exists")
        self.courses.append(Course(name, format))
        self.save_courses()

    def remove_course(self, name: str, format: str) -> None:
        """
        Removes a course from the tracker.

        Args:
            name (str): The name of the course.
            format (str): The format of the course (e.g., Online, Offline).
        """
        for course in self.courses:
            if course.name == name and course.format == format:
                self.courses.remove(course)
        self.save_courses()

    def get_course(self, name: str, format: str) -> Course:
        """
        Retrieves a course by name and format.

        Args:
            name (str): The name of the course.
            format (str): The format of the course (e.g., Online, Offline).

        Returns:
            Course: The course object matching the name and format.

        Raises:
            ValueError: If the course does not exist.
        """
        for course in self.courses:
            if course.name == name and course.format == format:
                return course
        raise ValueError("This course doesn't exist")

    def list_courses(self) -> list[Course]:
        """
        Returns a list of all courses being tracked.

        Returns:
            list[Course]: A list of all courses being tracked.
        """
        return self.courses

    def list_courses_str(self) -> list[str]:
        """
        Returns a list of all course names as strings.

        Returns:
            list[str]: A list of string representations of all courses.
        """
        return [str(course) for course in self.courses]

    def increment_unattended(self, name: str, format: str) -> None:
        """
        Increments unattended classes for a specific course.

        Args:
            name (str): The name of the course.
            format (str): The format of the course (e.g., Online, Offline).
        """
        for course in self.courses:
            if course.name == name and course.format == format:
                course.increment_un_classes()
        self.save_courses()

    def decrement_unattended(self, name: str, format: str) -> None:
        """
        Decrements unattended classes for a specific course.

        Args:
            name (str): The name of the course.
            format (str): The format of the course (e.g., Online, Offline).
        """
        for course in self.courses:
            if course.name == name and course.format == format:
                course.decrement_un_classes()
        self.save_courses()

    def save_courses(self) -> None:
        """
        Saves the current list of courses to a file.
        """
        with open(self.filename, "wb") as f:
            pickle.dump(self.courses, f)

    def load_courses(self) -> list[Course]:
        """
        Loads the list of courses from a file.

        Returns:
            list[Course]: The list of courses loaded from the file. Returns an empty list if the file does not exist or is corrupted.
        """
        if not os.path.exists(self.filename):
            print(f"File {self.filename} does not exist. Returning an empty list.")
            return []

        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except pickle.UnpicklingError:
            print(
                f"Error unpickling {self.filename}. File may be corrupted. Returning an empty list."
            )
            return []
        except Exception as e:
            print(
                f"An error occurred while loading {self.filename}: {str(e)}. Returning an empty list."
            )
            return []
