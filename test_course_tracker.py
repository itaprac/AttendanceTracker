import pytest
from course_tracker import CourseTracker


@pytest.fixture
def course_tracker(tmp_path):
    # Create a temporary file for testing
    filename = tmp_path / "courses.pkl"
    return CourseTracker(filename=str(filename))


def test_initialization(course_tracker):
    assert course_tracker.courses == []


def test_add_course(course_tracker):
    course_tracker.add_course("Math", "Online")
    assert len(course_tracker.courses) == 1
    assert course_tracker.courses[0].name == "Math"
    assert course_tracker.courses[0].format == "Online"


def test_remove_course(course_tracker):
    course_tracker.add_course("Math", "Online")
    course_tracker.remove_course("Math", "Online")
    assert len(course_tracker.courses) == 0


def test_get_course(course_tracker):
    course_tracker.add_course("Math", "Online")
    course = course_tracker.get_course("Math", "Online")
    assert course.name == "Math"
    assert course.format == "Online"
    with pytest.raises(ValueError):
        course_tracker.get_course("Science", "Offline")


def test_list_courses_str(course_tracker):
    course_tracker.add_course("Math", "Online")
    course_tracker.add_course("Science", "Offline")
    courses_str = course_tracker.list_courses_str()
    assert len(courses_str) == 2
    assert "Course: Math, Format: Online, Unattended Classes: 0" in courses_str
    assert "Course: Science, Format: Offline, Unattended Classes: 0" in courses_str


def test_increment_unattended(course_tracker):
    course_tracker.add_course("Math", "Online")
    course_tracker.increment_unattended("Math", "Online")
    assert course_tracker.courses[0].un_classes == 1


def test_decrement_unattended(course_tracker):
    course_tracker.add_course("Math", "Online")
    course_tracker.increment_unattended("Math", "Online")
    course_tracker.decrement_unattended("Math", "Online")
    assert course_tracker.courses[0].un_classes == 0


def test_save_and_load_courses(course_tracker, tmp_path):
    course_tracker.add_course("Math", "Online")
    course_tracker.save_courses()
    new_tracker = CourseTracker(filename=str(tmp_path / "courses.pkl"))
    assert len(new_tracker.courses) == 1
    assert new_tracker.courses[0].name == "Math"
    assert new_tracker.courses[0].format == "Online"
