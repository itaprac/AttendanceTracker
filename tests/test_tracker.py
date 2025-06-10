import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_tracker import CourseTracker


def test_add_and_remove_course(tmp_path):
    tracker = CourseTracker(db_directory=tmp_path)
    tracker.add_course("Algebra", "Wykład")
    assert len(tracker.list_courses()) == 1
    tracker.remove_course("Algebra", "Wykład")
    assert len(tracker.list_courses()) == 0


def test_export_and_import(tmp_path):
    tracker = CourseTracker(db_directory=tmp_path)
    tracker.add_course("Algebra", "Wykład", un_classes=2)
    csv_file = tmp_path / "out.csv"
    tracker.export_courses(csv_file)
    assert csv_file.exists()

    tracker.reset_data()
    assert len(tracker.list_courses()) == 0

    tracker.import_courses_replace(csv_file)
    assert len(tracker.list_courses()) == 1
    course = tracker.list_courses()[0]
    assert course.name == "Algebra"
    assert course.format == "Wykład"
    assert course.un_classes == 2
