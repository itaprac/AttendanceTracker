import tkinter as tk
from tkinter import ttk, messagebox
from course_tracker import CourseTracker


class CourseTrackerGUI:
    """
    A class to create a GUI for tracking courses and their unattended classes.
    """

    def __init__(self, master):
        """
        Initializes the CourseTrackerGUI with the master window.

        Args:
            master (tk.Tk): The root window of the Tkinter application.
        """
        self.master = master
        self.master.title("Śledzenie Frekwencji Kursów")
        self.tracker = CourseTracker()

        # Bind keybinds
        self.bind_shortcuts()

        # Create and set up the GUI elements
        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI elements.
        """
        # Frame for adding new courses
        add_frame = ttk.LabelFrame(self.master, text="Dodaj nowy kurs")
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Entry fields for course name and format, and an "Add" button
        self.course_name_label = ttk.Label(add_frame, text="Nazwa kursu")
        self.course_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.course_name_entry = ttk.Entry(add_frame)
        self.course_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Create a label for the dropdown
        self.dropdown_label = ttk.Label(add_frame, text="Format:")
        self.dropdown_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Create the dropdown (Combobox)
        self.categories = ["Audytorium", "Wykład", "Laboratorium"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            add_frame, textvariable=self.category_var, values=self.categories
        )
        self.category_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.category_dropdown.set("Audytorium")
        self.category_dropdown["state"] = "readonly"

        self.add_button = ttk.Button(
            add_frame,
            text="Dodaj",
            command=self.add_course,
        )
        self.add_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        # Frame for listing courses
        list_frame = ttk.LabelFrame(self.master, text="Lista Kursów")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create a Treeview widget
        self.courses_tree = ttk.Treeview(
            list_frame,
            columns=("Name", "Format", "Unattended Classes"),
            show="headings",
        )
        self.courses_tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.courses_tree.heading("Name", text="Kurs")
        self.courses_tree.heading("Format", text="Format")
        self.courses_tree.heading("Unattended Classes", text="Opuszczone")

        self.courses_tree.column("Name", width=150)
        self.courses_tree.column("Format", width=150)
        self.courses_tree.column("Unattended Classes", width=100)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.courses_tree.yview
        )
        scrollbar.grid(row=0, column=3, sticky="ns")
        self.courses_tree.configure(yscrollcommand=scrollbar.set)

        # Make the treeview expandable
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        self.list_courses()

        # Variable to store the selected item
        self.selected_item = None
        self.courses_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create a frame for buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=3, padx=100, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.delete_button = ttk.Button(
            button_frame,
            text="Usuń Kurs",
            command=lambda: self.delete_course(),
            width=10,
        )
        self.delete_button.grid(row=0, column=2, padx=0, pady=0)
        self.delete_button.config(state="disabled")

        self.increment_button = ttk.Button(
            button_frame,
            text="+",
            command=lambda: self.increment_unattended(),
            width=10,
        )
        self.increment_button.grid(row=0, column=1, padx=0, pady=0)
        self.increment_button.config(state="disabled")

        self.decrement_button = ttk.Button(
            button_frame,
            text="-",
            command=lambda: self.decrement_unattended(),
            width=10,
        )
        self.decrement_button.grid(row=0, column=0, padx=0, pady=0)
        self.decrement_button.config(state="disabled")

    def add_course(self):
        """
        Adds a new course to the tracker and updates the course list.
        """
        course_name = self.course_name_entry.get()
        format = self.category_var.get()
        if course_name:
            try:
                self.tracker.add_course(course_name, format)
                self.course_name_entry.delete(0, tk.END)
                self.list_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Nie udało się dodać kursu: {str(e)}")
        else:
            messagebox.showerror("Error", "Proszę wprowadzić nazwę kursu.")

    def list_courses(self):
        """
        Lists all courses in the Treeview widget.
        """
        # Clear all items from the Treeview
        self.courses_tree.delete(*self.courses_tree.get_children())
        courses = self.tracker.list_courses()
        for course in courses:
            self.courses_tree.insert(
                "", "end", values=(course.name, course.format, course.un_classes)
            )

    def delete_course(self):
        """
        Deletes the selected course from the tracker and updates the course list.
        """
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name = values[0]
            course_format = values[1]
            # print(f"Deleting course: {course_name} {course_format}")
            if messagebox.askyesno(
                "Potwierdzenie Usunięcia", f"Czy na pewno chcesz usunąć {course_name}?"
            ):
                try:
                    self.tracker.remove_course(course_name, course_format)
                    self.courses_tree.delete(self.selected_item)
                    self.selected_item = None
                    self.update_button_states()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Nie udało się usunąć kursu: {str(e)}"
                    )

    def increment_unattended(self):
        """
        Increments the unattended classes for the selected course and updates the course list.
        """
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name = values[0]
            course_format = values[1]
            self.tracker.increment_unattended(course_name, course_format)
            self.list_courses()

    def decrement_unattended(self):
        """
        Decrements the unattended classes for the selected course and updates the course list.
        """
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name = values[0]
            course_format = values[1]
            self.tracker.decrement_unattended(course_name, course_format)
            self.list_courses()

    def update_button_states(self):
        """
        Updates the states of the buttons based on the selected item in the Treeview.
        """
        if self.selected_item:
            self.delete_button.config(state="normal")
            self.increment_button.config(state="normal")
            self.decrement_button.config(state="normal")
        else:
            self.delete_button.config(state="disabled")
            self.increment_button.config(state="disabled")
            self.decrement_button.config(state="disabled")

    def on_tree_select(self, event):
        """
        Handles the selection event in the Treeview.

        Args:
            event (tk.Event): The event object.
        """
        selected_items = self.courses_tree.selection()
        if selected_items:
            self.selected_item = selected_items[0]
        else:
            self.selected_item = None
        self.update_button_states()

    def bind_shortcuts(self):
        self.master.bind("<BackSpace>", lambda event: self.delete_course())
        self.master.bind("<Delete>", lambda event: self.delete_course())


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseTrackerGUI(root)
    root.mainloop()
