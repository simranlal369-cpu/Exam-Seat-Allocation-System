"""Exam Seat Allocation System - Tkinter GUI with SQLite database."""

import random
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DATABASE_NAME = "exam_seating.db"
BACKGROUND = "#f2f5f9"
HEADER = "#243b55"


class ExamSeatAllocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Seat Allocation System")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BACKGROUND)

        self.conn = sqlite3.connect(DATABASE_NAME)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.build_interface()
        self.view_students()
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def create_tables(self):
        """Create the required database tables if they do not exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    roll_no TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    room_no TEXT PRIMARY KEY,
                    capacity INTEGER NOT NULL CHECK (capacity > 0)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS allocations (
                    roll_no TEXT PRIMARY KEY,
                    room_no TEXT NOT NULL,
                    seat_no INTEGER NOT NULL CHECK (seat_no > 0),
                    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
                        ON DELETE CASCADE,
                    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
                        ON DELETE CASCADE,
                    UNIQUE (room_no, seat_no)
                )
            """)

    def build_interface(self):
        title = tk.Label(
            self.root, text="EXAM SEAT ALLOCATION SYSTEM",
            font=("Arial", 20, "bold"), bg=HEADER, fg="white", pady=16
        )
        title.pack(fill="x")

        input_frame = tk.LabelFrame(
            self.root, text="Student and Room Details",
            font=("Arial", 10, "bold"), bg=BACKGROUND, padx=12, pady=10
        )
        input_frame.pack(fill="x", padx=20, pady=15)

        self.roll_entry = self.add_labeled_entry(input_frame, "Roll Number:", 0, 0)
        self.name_entry = self.add_labeled_entry(input_frame, "Student Name:", 0, 2)
        self.course_entry = self.add_labeled_entry(input_frame, "Course:", 1, 0)
        self.room_entry = self.add_labeled_entry(input_frame, "Room Number:", 1, 2)
        self.capacity_entry = self.add_labeled_entry(input_frame, "Room Capacity:", 2, 2)

        table_frame = tk.Frame(self.root, bg=BACKGROUND)
        table_frame.pack(fill="both", expand=True, padx=20, pady=5)
        columns = ("Roll No", "Student Name", "Course", "Room No", "Seat No")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=170, anchor="center")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        button_frame = tk.Frame(self.root, bg=BACKGROUND)
        button_frame.pack(pady=12)
        buttons = [
            ("Add Student", self.add_student, "#287a4b"),
            ("Add Room", self.add_room, "#287a4b"),
            ("View Students", self.view_students, "#2867a5"),
            ("Allocate Seats", self.allocate_seats, "#a65a17"),
            ("View Allocations", self.view_allocations, "#2867a5"),
            ("Search Student", self.search_student, "#6a42a5"),
            ("Clear Table", self.clear_table, "#555555"),
            ("Exit", self.close_application, "#b52b35"),
        ]
        for index, (label, command, color) in enumerate(buttons):
            row, column = divmod(index, 4)
            tk.Button(
                button_frame, text=label, command=command, width=17,
                bg=color, fg="white", activebackground=color,
                activeforeground="white", relief="flat", cursor="hand2",
                padx=5, pady=7
            ).grid(row=row, column=column, padx=6, pady=5)

        self.status_label = tk.Label(
            self.root, text="Ready", anchor="w", bg="#e3eaf2",
            fg=HEADER, padx=12, pady=5
        )
        self.status_label.pack(fill="x", side="bottom")

    @staticmethod
    def add_labeled_entry(parent, label_text, row, column):
        tk.Label(parent, text=label_text, bg=BACKGROUND, anchor="w").grid(
            row=row, column=column, padx=6, pady=7, sticky="w"
        )
        entry = tk.Entry(parent, width=24)
        entry.grid(row=row, column=column + 1, padx=6, pady=7, sticky="ew")
        return entry

    def set_status(self, message):
        self.status_label.config(text=message)

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.set_status("Table cleared.")

    def clear_student_fields(self):
        for entry in (self.roll_entry, self.name_entry, self.course_entry):
            entry.delete(0, tk.END)

    def clear_room_fields(self):
        self.room_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)

    def add_student(self):
        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        course = self.course_entry.get().strip()
        if not all((roll, name, course)):
            messagebox.showwarning(
                "Missing Information",
                "Please enter the roll number, student name, and course."
            )
            return
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO students (roll_no, name, course) VALUES (?, ?, ?)",
                    (roll, name, course)
                )
            self.clear_student_fields()
            self.view_students()
            self.set_status(f"Student {roll} added successfully.")
            messagebox.showinfo("Success", "Student added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Roll Number", "A student with this roll number already exists."
            )
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def add_room(self):
        room = self.room_entry.get().strip()
        capacity_text = self.capacity_entry.get().strip()
        if not room or not capacity_text:
            messagebox.showwarning(
                "Missing Information", "Please enter the room number and room capacity."
            )
            return
        try:
            capacity = int(capacity_text)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Capacity", "Room capacity must be a positive whole number."
            )
            return
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO rooms (room_no, capacity) VALUES (?, ?)",
                    (room, capacity)
                )
            self.clear_room_fields()
            self.set_status(f"Room {room} added with capacity {capacity}.")
            messagebox.showinfo("Success", "Examination room added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Room", "A room with this room number already exists."
            )
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def display_records(self, records):
        self.clear_table()
        for record in records:
            self.table.insert("", tk.END, values=record)
        self.set_status(f"{len(records)} record(s) displayed.")

    def view_students(self):
        try:
            records = self.conn.execute("""
                SELECT roll_no, name, course, '-', '-'
                FROM students ORDER BY roll_no
            """).fetchall()
            self.display_records(records)
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def view_allocations(self):
        try:
            records = self.conn.execute("""
                SELECT s.roll_no, s.name, s.course, a.room_no, a.seat_no
                FROM allocations AS a
                JOIN students AS s ON s.roll_no = a.roll_no
                ORDER BY a.room_no, a.seat_no
            """).fetchall()
            self.display_records(records)
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def allocate_seats(self):
        """Randomly assign one valid seat to every student."""
        try:
            students = self.conn.execute(
                "SELECT roll_no FROM students ORDER BY roll_no"
            ).fetchall()
            rooms = self.conn.execute(
                "SELECT room_no, capacity FROM rooms ORDER BY room_no"
            ).fetchall()

            if not students:
                messagebox.showwarning(
                    "No Students", "Please add students before allocating seats."
                )
                return
            if not rooms:
                messagebox.showwarning(
                    "No Rooms", "Please add examination rooms first."
                )
                return

            total_capacity = sum(capacity for _, capacity in rooms)
            if len(students) > total_capacity:
                messagebox.showerror(
                    "Insufficient Seats",
                    f"Students: {len(students)}\nAvailable seats: {total_capacity}\n\n"
                    "Please add more rooms or increase room capacity."
                )
                return

            roll_numbers = [row[0] for row in students]
            random.shuffle(roll_numbers)
            new_allocations = []
            student_index = 0

            for room_no, capacity in rooms:
                for seat_no in range(1, capacity + 1):
                    if student_index >= len(roll_numbers):
                        break
                    new_allocations.append(
                        (roll_numbers[student_index], room_no, seat_no)
                    )
                    student_index += 1
                if student_index >= len(roll_numbers):
                    break

            # Delete old allocations and insert new ones atomically.
            with self.conn:
                self.conn.execute("DELETE FROM allocations")
                self.conn.executemany(
                    """INSERT INTO allocations (roll_no, room_no, seat_no)
                       VALUES (?, ?, ?)""",
                    new_allocations
                )

            self.view_allocations()
            self.set_status(f"Allocated seats to {len(new_allocations)} student(s).")
            messagebox.showinfo(
                "Allocation Complete",
                "Seat allocation completed successfully!\n"
                f"Students allocated: {len(new_allocations)}"
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Allocation Error", f"The allocation could not be saved:\n{error}"
            )

    def search_student(self):
        roll = self.roll_entry.get().strip()
        if not roll:
            messagebox.showwarning(
                "Input Required",
                "Enter the student's roll number in the Roll Number field."
            )
            return
        try:
            record = self.conn.execute("""
                SELECT s.roll_no, s.name, s.course,
                       COALESCE(a.room_no, '-'),
                       COALESCE(CAST(a.seat_no AS TEXT), '-')
                FROM students AS s
                LEFT JOIN allocations AS a ON s.roll_no = a.roll_no
                WHERE s.roll_no = ?
            """, (roll,)).fetchone()
            if record:
                self.display_records([record])
            else:
                self.clear_table()
                self.set_status(f"No student found for roll number {roll}.")
                messagebox.showinfo(
                    "Not Found", "No student found with this roll number."
                )
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def close_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to close the application?"):
            self.conn.close()
            self.root.destroy()


def main():
    root = tk.Tk()
    ExamSeatAllocationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
