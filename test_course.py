import pytest
from course import Course


def test_initialization():
    course = Course(name="Math", format="Online", un_classes=1)
    assert course.name == "Math"
    assert course.format == "Online"
    assert course.un_classes == 1


def test_initialization_with_invalid_un_classes():
    course = Course(name="Math", format="Online", un_classes=3)
    assert course.un_classes == 3
    course = Course(name="Math", format="Online", un_classes=-1)
    assert course.un_classes == 0


def test_name_property():
    course = Course(name="Math", format="Online")
    course.name = "Science"
    assert course.name == "Science"


def test_format_property():
    course = Course(name="Math", format="Online")
    course.format = "Offline"
    assert course.format == "Offline"


def test_un_classes_property():
    course = Course(name="Math", format="Online")
    course.un_classes = 3
    assert course.un_classes == 3
    course.un_classes = 3
    assert course.un_classes == 3
    course.un_classes = -1
    assert course.un_classes == 0


def test_increment_un_classes():
    course = Course(name="Math", format="Online", un_classes=0)
    course.increment_un_classes()
    assert course.un_classes == 1
    course.increment_un_classes(3)
    assert course.un_classes == 3
    with pytest.raises(ValueError):
        course.increment_un_classes(-1)


def test_decrement_un_classes():
    course = Course(name="Math", format="Online", un_classes=3)
    course.decrement_un_classes()
    assert course.un_classes == 2
    course.decrement_un_classes(3)
    assert course.un_classes == 0
    with pytest.raises(ValueError):
        course.decrement_un_classes(-1)


def test_str_method():
    course = Course(name="Math", format="Online", un_classes=1)
    assert str(course) == "Course: Math, Format: Online, Unattended Classes: 1"
