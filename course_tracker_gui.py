import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from course_tracker import CourseTracker
import platform


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
        self.selected_item = None

        # writer test
        # self.tracker.export_courses("test.csv")
        # self.tracker.courses = self.tracker.import_courses("test.csv")

        # Make window resizable
        self.master.geometry("750x400")
        self.master.minsize(700, 370)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        # Create the menu bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # Create the File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Add Import and Export options to the File menu
        file_menu.add_command(label="Import", command=self.import_file)
        file_menu.add_command(label="Export", command=self.export_file)
        file_menu.add_command(label="Reset all data", command=self.reset_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        file_menu.add_command(
            label="Close", accelerator="Cmd+W", command=self.close_window
        )
        file_menu.add_command(label="Quit", accelerator="Cmd+Q", command=root.quit)

        # Bind keybinds
        self.bind_shortcuts()

        # Center window
        self.center_window()

        # Create and set up the GUI elements
        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI elements.
        """
        # Frame for adding new courses
        add_frame = ttk.LabelFrame(self.master, text="Dodaj nowy kurs")
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.columnconfigure(1, weight=1)  # Make the course name entry expandable
        add_frame.columnconfigure(3, weight=1)  # Make the dropdown expandable

        # Entry fields for course name and format, and an "Add" button
        self.course_name_label = ttk.Label(add_frame, text="Nazwa kursu")
        self.course_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.course_name_entry = ttk.Entry(add_frame)
        self.course_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Create a label for the dropdown
        self.dropdown_label = ttk.Label(add_frame, text="Format:")
        self.dropdown_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Create the dropdown (Combobox)
        self.categories = ["Audytorium", "Wykład", "Laboratorium"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            add_frame, textvariable=self.category_var, values=self.categories
        )
        self.category_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
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
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

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

        self.courses_tree.column("Name", width=150, stretch=tk.YES)
        self.courses_tree.column("Format", width=150, stretch=tk.YES)
        self.courses_tree.column("Unattended Classes", width=100, stretch=tk.YES)

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
        self.courses_tree.bind("<Button-1>", self.on_tree_click)

        # Setup tags (colors)
        self.setup_treeview_tags()

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

        # Make sure the list_frame expands properly
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

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

    def list_courses(self, select_item=None):
        """
        Lists all courses in the Treeview widget.
        """
        # Store the current selection if no specific item is to be selected
        if not select_item and self.selected_item:
            current_values = self.courses_tree.item(self.selected_item, "values")
            select_item = (current_values[0], current_values[1])  # (name, format)

        # Clear all items from the Treeview
        self.courses_tree.delete(*self.courses_tree.get_children())

        courses = self.tracker.list_courses()
        for course in courses:
            tag = self.get_attendance_tag(course.un_classes)
            item = self.courses_tree.insert(
                "",
                "end",
                values=(course.name, course.format, course.un_classes),
                tags=(tag,),
            )
            # If this is the item we want to select, store its ID
            if select_item and (course.name, course.format) == select_item:
                self.selected_item = item

        # Restore the selection
        if self.selected_item:
            self.courses_tree.selection_set(self.selected_item)
            self.courses_tree.see(
                self.selected_item
            )  # Ensure the selected item is visible

    def delete_course(self):
        """
        Deletes the selected course from the tracker and updates the course list.
        """
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name = values[0]
            course_format = values[1]
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
            self.list_courses((course_name, course_format))
            self.courses_tree.focus_set()

    def decrement_unattended(self):
        """
        Decrements the unattended classes for the selected course and updates the course list.
        """
        if self.selected_item:
            values = self.courses_tree.item(self.selected_item, "values")
            course_name = values[0]
            course_format = values[1]
            self.tracker.decrement_unattended(course_name, course_format)
            self.list_courses((course_name, course_format))
            self.courses_tree.focus_set()

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
        selected_items = self.courses_tree.selection()
        if selected_items:
            self.selected_item = selected_items[0]
        else:
            self.selected_item = None
        self.update_button_states()

    def on_tree_click(self, event):
        region = self.courses_tree.identify("region", event.x, event.y)
        if region == "nothing":
            # Click was on empty space
            self.deselect_item()

    def deselect_item(self, event=None):
        """
        Deselects the currently selected item in the Treeview.
        """
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

    # def bind_shortcuts(self):
    #     self.master.bind("<BackSpace>", lambda event: self.delete_course())
    #     self.master.bind("<Delete>", lambda event: self.delete_course())
    #     self.master.bind("<Left>", lambda event: self.decrement_unattended())
    #     self.master.bind("<Right>", lambda event: self.increment_unattended())
    #     self.master.bind("<Up>", lambda event: self.move_selection(-1))
    #     self.master.bind("<Down>", lambda event: self.move_selection(1))
    #     self.master.bind("<Escape>", self.deselect_item)
    #     self.master.bind("<Command-o>", self.import_file())
    # self.master.bind("<Command-s>", self.export_file())
    # self.master.bind("<Command-w>", self.close_window)
    # self.master.bind("<Command-q>", lambda e: root.quit())

    def bind_shortcuts(self):
        # Common shortcuts for all platforms
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
            self.master.bind("<Delete>", lambda event: self.delete_course())
            self.master.bind("<Control-o>", self.import_file)
            self.master.bind("<Control-s>", self.export_file)

    def center_window(self):
        # Update the idle tasks to make sure the window size is calculated
        self.master.update_idletasks()

        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the center of the screen
        x = (screen_width // 2) - (self.master.winfo_width() // 2)
        y = (screen_height // 2) - (self.master.winfo_height() // 2)

        # Set the position of the window to the center of the screen
        self.master.geometry(f"+{x}+{y}")

    def setup_treeview_tags(self):
        self.courses_tree.tag_configure("green", background="#90EE90")  # Light green
        self.courses_tree.tag_configure("yellow", background="#faf86e")  # Light yellow
        self.courses_tree.tag_configure("orange", background="#f5b127")  # Light orange
        self.courses_tree.tag_configure("red", background="#ff4051")  # Light red

    def get_attendance_tag(self, un_classes):
        if un_classes == 0:
            return "green"
        elif un_classes == 1:
            return "yellow"
        elif un_classes == 2:
            return "orange"
        else:
            return "red"

    def import_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            response = messagebox.askyesnocancel(
                "Import Options",
                "Do you want to replace the existing configuration?\n\n"
                "Yes: Replace existing configuration\n"
                "No: Append to existing configuration\n"
                "Cancel: Abort import",
            )

            if response is None:  # User clicked Cancel
                print("Import cancelled")
            elif response:  # User clicked Yes
                print(f"Replacing existing configuration with: {file_path}")
                self.tracker.import_courses_replace(file_path)
            else:  # User clicked No
                print(f"Appending to existing configuration from: {file_path}")
                self.tracker.import_courses_append(file_path)
        self.list_courses()

    def export_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("Csv files", "*.csv"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.tracker.export_courses(file_path)
            print(f"Exporting file: {file_path}")

    def close_window(self, event=None):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.quit()

    def reset_data(self):
        if messagebox.askokcancel(
            "Reset Data",
            "Czy napewno chcesz zresetowac dane? To operacja jest nieodwracalna!",
        ):
            self.tracker.reset_data()
            self.list_courses()


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseTrackerGUI(root)
    root.mainloop()
