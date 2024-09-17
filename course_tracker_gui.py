import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from course_tracker import CourseTracker
import platform


class CourseTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title(("Course Attendance Tracker"))
        self.tracker = CourseTracker()
        self.selected_item = None

        self.master.geometry("750x400")
        self.master.minsize(700, 370)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        self.setup_menu()
        self.bind_shortcuts()
        self.center_window()
        self.setup_gui()

    def setup_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=("File"), menu=file_menu)

        file_menu.add_command(label=("Import"), command=self.import_file)
        file_menu.add_command(label=("Export"), command=self.export_file)
        file_menu.add_command(label=("Reset all data"), command=self.reset_data)
        file_menu.add_separator()
        file_menu.add_command(
            label=("Close"), accelerator="Cmd+W", command=self.close_window
        )
        file_menu.add_command(
            label=("Exit"), accelerator="Cmd+Q", command=self.master.quit
        )

    def setup_gui(self):
        add_frame = ttk.LabelFrame(self.master, text=("Add new course"))
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(3, weight=1)

        ttk.Label(add_frame, text=("Course name")).grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.course_name_entry = ttk.Entry(add_frame)
        self.course_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_frame, text=("Format:")).grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )

        self.categories = [("Auditorium"), ("Lecture"), ("Laboratory")]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            add_frame,
            textvariable=self.category_var,
            values=self.categories,
            state="readonly",
        )
        self.category_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.category_dropdown.set(("Auditorium"))

        ttk.Button(add_frame, text=("Add"), command=self.add_course).grid(
            row=0, column=4, padx=5, pady=5, sticky="w"
        )

        list_frame = ttk.LabelFrame(self.master, text=("Course List"))
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.courses_tree = ttk.Treeview(
            list_frame,
            columns=("Name", "Format", "Unattended Classes"),
            show="headings",
        )
        self.courses_tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.courses_tree.heading("Name", text=("Course"))
        self.courses_tree.heading("Format", text=("Format"))
        self.courses_tree.heading("Unattended Classes", text=("Unattended"))

        self.courses_tree.column("Name", width=150, stretch=tk.YES)
        self.courses_tree.column("Format", width=150, stretch=tk.YES)
        self.courses_tree.column("Unattended Classes", width=100, stretch=tk.YES)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.courses_tree.yview
        )
        scrollbar.grid(row=0, column=3, sticky="ns")
        self.courses_tree.configure(yscrollcommand=scrollbar.set)

        self.courses_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.courses_tree.bind("<Button-1>", self.on_tree_click)

        self.setup_treeview_tags()

        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=3, padx=100, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.delete_button = ttk.Button(
            button_frame,
            text=("Delete Course"),
            command=self.delete_course,
            width=10,
            state="disabled",
        )
        self.delete_button.grid(row=0, column=2, padx=0, pady=0)

        self.increment_button = ttk.Button(
            button_frame,
            text="+",
            command=self.increment_unattended,
            width=10,
            state="disabled",
        )
        self.increment_button.grid(row=0, column=1, padx=0, pady=0)

        self.decrement_button = ttk.Button(
            button_frame,
            text="-",
            command=self.decrement_unattended,
            width=10,
            state="disabled",
        )
        self.decrement_button.grid(row=0, column=0, padx=0, pady=0)

        self.list_courses()

    def add_course(self):
        course_name = self.course_name_entry.get()
        format = self.category_var.get()
        if course_name:
            try:
                self.tracker.add_course(course_name, format)
                self.course_name_entry.delete(0, tk.END)
                self.list_courses()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać kursu: {str(e)}")
        else:
            messagebox.showerror("Błąd", "Proszę wprowadzić nazwę kursu.")

    def list_courses(self, select_item=None):
        if not select_item and self.selected_item:
            current_values = self.courses_tree.item(self.selected_item, "values")
            select_item = (current_values[0], current_values[1])

        self.courses_tree.delete(*self.courses_tree.get_children())

        for course in self.tracker.list_courses():
            tag = self.get_attendance_tag(course.un_classes)
            item = self.courses_tree.insert(
                "",
                "end",
                values=(course.name, course.format, course.un_classes),
                tags=(tag,),
            )
            if select_item and (course.name, course.format) == select_item:
                self.selected_item = item

        if self.selected_item:
            self.courses_tree.selection_set(self.selected_item)
            self.courses_tree.see(self.selected_item)

    def delete_course(self):
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name, course_format = values[0], values[1]
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
                        "Błąd", f"Nie udało się usunąć kursu: {str(e)}"
                    )

    def increment_unattended(self):
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name, course_format = values[0], values[1]
            self.tracker.increment_unattended(course_name, course_format)
            self.list_courses((course_name, course_format))
            self.courses_tree.focus_set()

    def decrement_unattended(self):
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name, course_format = values[0], values[1]
            self.tracker.decrement_unattended(course_name, course_format)
            self.list_courses((course_name, course_format))
            self.courses_tree.focus_set()

    def update_button_states(self):
        state = "normal" if self.selected_item else "disabled"
        self.delete_button.config(state=state)
        self.increment_button.config(state=state)
        self.decrement_button.config(state=state)

    def on_tree_select(self, event):
        selected_items = self.courses_tree.selection()
        self.selected_item = selected_items[0] if selected_items else None
        self.update_button_states()

    def on_tree_click(self, event):
        if self.courses_tree.identify("region", event.x, event.y) == "nothing":
            self.deselect_item()

    def deselect_item(self, event=None):
        self.courses_tree.selection_remove(self.courses_tree.selection())
        self.selected_item = None
        self.update_button_states()
        self.courses_tree.focus_set()

    def move_selection(self, direction):
        if self.selected_item:
            items = self.courses_tree.get_children()
            current_index = items.index(self.selected_item)
            new_index = (current_index + direction) % len(items)
            new_item = items[new_index]
            self.courses_tree.selection_set(new_item)
            self.courses_tree.see(new_item)
            self.selected_item = new_item
            self.update_button_states()

    def bind_shortcuts(self):
        self.master.bind("<Left>", lambda event: self.decrement_unattended())
        self.master.bind("<Right>", lambda event: self.increment_unattended())
        self.master.bind("<Up>", lambda event: self.move_selection(-1))
        self.master.bind("<Down>", lambda event: self.move_selection(1))
        self.master.bind("<Escape>", self.deselect_item)

        if platform.system() == "Darwin":  # macOS
            self.master.bind("<Command-o>", self.import_file)
            self.master.bind("<Command-s>", self.export_file)
            self.master.bind("<Command-w>", self.close_window)
            self.master.bind("<Command-q>", lambda event: self.master.quit())
            self.master.bind("<BackSpace>", lambda event: self.delete_course())
        else:  # Windows and Linux
            self.master.bind("<Control-o>", self.import_file)
            self.master.bind("<Control-s>", self.export_file)
            self.master.bind("<Delete>", lambda event: self.delete_course())

    def center_window(self):
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (self.master.winfo_width() // 2)
        y = (screen_height // 2) - (self.master.winfo_height() // 2)
        self.master.geometry(f"+{x}+{y}")

    def setup_treeview_tags(self):
        self.courses_tree.tag_configure("green", background="#90EE90")
        self.courses_tree.tag_configure("yellow", background="#faf86e")
        self.courses_tree.tag_configure("orange", background="#f5b127")
        self.courses_tree.tag_configure("red", background="#ff4051")

    def get_attendance_tag(self, un_classes):
        return ["green", "yellow", "orange", "red"][
            min(un_classes, 3)
        ]  # ... (rest of the methods remain the same, just replace string literals with _("..."))

    def import_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[(("Text files"), "*.csv"), (("All files"), "*.*")]
        )
        if file_path:
            response = messagebox.askyesnocancel(
                ("Import options"),
                (
                    "Do you want to replace the existing configuration?\n\n"
                    "Yes: Replace existing configuration\n"
                    "No: Add to existing configuration\n"
                    "Cancel: Abort import"
                ),
            )
            if response is not None:
                if response:
                    self.tracker.import_courses_replace(file_path)
                else:
                    self.tracker.import_courses_append(file_path)
                self.list_courses()

    def export_file(self, event=None):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[(("CSV files"), "*.csv"), (("All files"), "*.*")],
        )
        if file_path:
            self.tracker.export_courses(file_path)

    def close_window(self, event=None):
        if messagebox.askokcancel(("Exit"), ("Do you want to exit the program?")):
            self.master.quit()

    def reset_data(self):
        if messagebox.askokcancel(
            ("Reset data"),
            (
                "Are you sure you want to reset the data? This operation is irreversible!"
            ),
        ):
            self.tracker.reset_data()
            self.list_courses()


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseTrackerGUI(root)
    root.mainloop()
