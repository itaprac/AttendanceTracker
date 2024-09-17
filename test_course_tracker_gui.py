import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from course_tracker_gui import CourseTrackerGUI


@pytest.fixture
def app():
    root = tk.Tk()
    app = CourseTrackerGUI(root)
    app.tracker = MagicMock()
    yield app
    root.destroy()


def test_add_course(app):
    app.course_name_entry.insert(0, "Test Course")
    app.category_var.set("Wykład")
    app.add_course()
    app.tracker.add_course.assert_called_with("Test Course", "Wykład")
    assert app.course_name_entry.get() == ""


def test_add_course_empty_name(app):
    app.course_name_entry.delete(0, tk.END)
    with patch("tkinter.messagebox.showerror") as mock_showerror:
        app.add_course()
        mock_showerror.assert_called_with("Błąd", "Proszę wprowadzić nazwę kursu.")


# def test_delete_course(app):
#     app.selected_item = "item1"
#     app.courses_tree.item = MagicMock(
#         return_value={"values": ("Test Course", "Wykład")}
#     )
#     with patch("tkinter.messagebox.askyesno", return_value=True):
#         app.delete_course()
#         app.tracker.remove_course.assert_called_with("Test Course", "Wykład")
#         assert app.selected_item is None
#
#
# def test_increment_unattended(app):
#     app.selected_item = "item1"
#     app.courses_tree.item = MagicMock(
#         return_value={"values": ("Test Course", "Wykład")}
#     )
#     app.increment_unattended()
#     app.tracker.increment_unattended.assert_called_with("Test Course", "Wykład")
#
#
# def test_decrement_unattended(app):
#     app.selected_item = "item1"
#     app.courses_tree.item = MagicMock(
#         return_value={"values": ("Test Course", "Wykład")}
#     )
#     app.decrement_unattended()
#     app.tracker.decrement_unattended.assert_called_with("Test Course", "Wykład")


def test_import_file(app):
    with patch("tkinter.filedialog.askopenfilename", return_value="test.csv"):
        with patch("tkinter.messagebox.askyesnocancel", return_value=True):
            app.import_file()
            app.tracker.import_courses_replace.assert_called_with("test.csv")


def test_export_file(app):
    with patch("tkinter.filedialog.asksaveasfilename", return_value="test.csv"):
        app.export_file()
        app.tracker.export_courses.assert_called_with("test.csv")


def test_reset_data(app):
    with patch("tkinter.messagebox.askokcancel", return_value=True):
        app.reset_data()
        app.tracker.reset_data.assert_called_once()
