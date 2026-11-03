import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random


# ==========================================
# 1. DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect("exam_seating.db")
cursor = conn.cursor()

# Student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT NOT NULL
)
""")

# Examination room table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_no TEXT PRIMARY KEY,
    capacity INTEGER NOT NULL
)
""")

# Seat allocation table
cursor.execute("""
CREATE TABLE IF NOT EXISTS allocations (
    roll_no TEXT PRIMARY KEY,
    room_no TEXT NOT NULL,
    seat_no INTEGER NOT NULL
)
""")

conn.commit()


# ==========================================
# 2. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Exam Seat Allocation System")
root.geometry("950x650")
root.configure(bg="#f2f5f9")


# ==========================================
# 3. TITLE
# ==========================================

title = tk.Label(
    root,
    text="EXAM SEAT ALLOCATION SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#243b55",
    fg="white",
    pady=15
)
title.pack(fill="x")


# ==========================================
# 4. INPUT FRAME
# ==========================================

input_frame = tk.Frame(root, bg="#f2f5f9")
input_frame.pack(pady=15)


# Student inputs
tk.Label(
    input_frame,
    text="Roll Number:",
    bg="#f2f5f9"
).grid(row=0, column=0, padx=5, pady=5, sticky="w")

roll_entry = tk.Entry(input_frame, width=22)
roll_entry.grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Student Name:",
    bg="#f2f5f9"
).grid(row=0, column=2, padx=5, pady=5, sticky="w")

name_entry = tk.Entry(input_frame, width=22)
name_entry.grid(row=0, column=3, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Course:",
    bg="#f2f5f9"
).grid(row=1, column=0, padx=5, pady=5, sticky="w")

course_entry = tk.Entry(input_frame, width=22)
course_entry.grid(row=1, column=1, padx=5, pady=5)


# Room inputs
tk.Label(
    input_frame,
    text="Room Number:",
    bg="#f2f5f9"
).grid(row=1, column=2, padx=5, pady=5, sticky="w")

room_entry = tk.Entry(input_frame, width=22)
room_entry.grid(row=1, column=3, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Room Capacity:",
    bg="#f2f5f9"
).grid(row=2, column=2, padx=5, pady=5, sticky="w")

capacity_entry = tk.Entry(input_frame, width=22)
capacity_entry.grid(row=2, column=3, padx=5, pady=5)


# ==========================================
# 5. DISPLAY TABLE
# ==========================================

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Roll No", "Student Name", "Course", "Room No", "Seat No")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=160, anchor="center")

table.pack(fill="both", expand=True)


# ==========================================
# 6. CLEAR DISPLAY TABLE
# ==========================================

def clear_table():
    for item in table.get_children():
        table.delete(item)


# ==========================================
# 7. ADD STUDENT
# ==========================================

def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()

    if not roll or not name or not course:
        messagebox.showwarning(
            "Missing Information",
            "Please enter roll number, name, and course."
        )
        return

    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (roll, name, course)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)

        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This roll number already exists."
        )


# ==========================================
# 8. ADD EXAMINATION ROOM
# ==========================================

def add_room():
    room = room_entry.get().strip()
    capacity = capacity_entry.get().strip()

    if not room or not capacity:
        messagebox.showwarning(
            "Missing Information",
            "Please enter room number and capacity."
        )
        return

    try:
        capacity = int(capacity)

        if capacity <= 0:
            messagebox.showerror(
                "Invalid Capacity",
                "Capacity must be greater than zero."
            )
            return

        cursor.execute(
            "INSERT INTO rooms VALUES (?, ?)",
            (room, capacity)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Examination room added successfully!"
        )

        room_entry.delete(0, tk.END)
        capacity_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Room capacity must be a whole number."
        )

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This room number already exists."
        )


# ==========================================
# 9. VIEW ALL STUDENTS
# ==========================================

def view_students():
    clear_table()

    cursor.execute("""
        SELECT roll_no, name, course
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    for student in students:
        table.insert(
            "",
            tk.END,
            values=(student[0], student[1], student[2], "-", "-")
        )


# ==========================================
# 10. GENERATE SEAT ALLOCATION
# ==========================================

def allocate_seats():
    cursor.execute("""
        SELECT roll_no, name, course
        FROM students
    """)

    students = cursor.fetchall()

    cursor.execute("""
        SELECT room_no, capacity
        FROM rooms
        ORDER BY room_no
    """)

    rooms = cursor.fetchall()

    if not students:
        messagebox.showwarning(
            "No Students",
            "Please add students before allocating seats."
        )
        return

    if not rooms:
        messagebox.showwarning(
            "No Rooms",
            "Please add examination rooms first."
        )
        return

    total_capacity = sum(room[1] for room in rooms)

    if len(students) > total_capacity:
        messagebox.showerror(
            "Insufficient Seats",
            f"Students: {len(students)}\n"
            f"Available seats: {total_capacity}\n\n"
            "Please add more rooms or increase capacity."
        )
        return

    # Randomize the order of students
    random.shuffle(students)

    # Start a new allocation
    cursor.execute("DELETE FROM allocations")

    student_index = 0

    for room_no, capacity in rooms:

        for seat_no in range(1, capacity + 1):

            if student_index >= len(students):
                break

            roll_no = students[student_index][0]

            cursor.execute("""
                INSERT INTO allocations
                (roll_no, room_no, seat_no)
                VALUES (?, ?, ?)
            """, (roll_no, room_no, seat_no))

            student_index += 1

        if student_index >= len(students):
            break

    conn.commit()

    view_allocations()

    messagebox.showinfo(
        "Success",
        f"Seat allocation completed!\n"
        f"Students allocated: {len(students)}"
    )


# ==========================================
# 11. VIEW SEAT ALLOCATIONS
# ==========================================

def view_allocations():
    clear_table()

    cursor.execute("""
        SELECT
            students.roll_no,
            students.name,
            students.course,
            allocations.room_no,
            allocations.seat_no
        FROM students
        INNER JOIN allocations
        ON students.roll_no = allocations.roll_no
        ORDER BY allocations.room_no, allocations.seat_no
    """)

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)


# ==========================================
# 12. SEARCH STUDENT
# ==========================================

def search_student():
    roll = roll_entry.get().strip()

    if not roll:
        messagebox.showwarning(
            "Input Required",
            "Enter the student's roll number in the Roll Number field."
        )
        return

    clear_table()

    cursor.execute("""
        SELECT
            students.roll_no,
            students.name,
            students.course,
            allocations.room_no,
            allocations.seat_no
        FROM students
        LEFT JOIN allocations
        ON students.roll_no = allocations.roll_no
        WHERE students.roll_no = ?
    """, (roll,))

    record = cursor.fetchone()

    if record:
        table.insert("", tk.END, values=record)
    else:
        messagebox.showinfo(
            "Not Found",
            "No student found with this roll number."
        )


# ==========================================
# 13. BUTTONS
# ==========================================

button_frame = tk.Frame(root, bg="#f2f5f9")
button_frame.pack(pady=12)


tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=15,
    bg="#287a4b",
    fg="white"
).grid(row=0, column=0, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Add Room",
    command=add_room,
    width=15,
    bg="#287a4b",
    fg="white"
).grid(row=0, column=1, padx=5, pady=5)


tk.Button(
    button_frame,
    text="View Students",
    command=view_students,
    width=15,
    bg="#2867a5",
    fg="white"
).grid(row=0, column=2, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Allocate Seats",
    command=allocate_seats,
    width=15,
    bg="#a65a17",
    fg="white"
).grid(row=0, column=3, padx=5, pady=5)


tk.Button(
    button_frame,
    text="View Allocations",
    command=view_allocations,
    width=15,
    bg="#2867a5",
    fg="white"
).grid(row=1, column=0, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Search Student",
    command=search_student,
    width=15,
    bg="#6a42a5",
    fg="white"
).grid(row=1, column=1, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Clear Table",
    command=clear_table,
    width=15,
    bg="#555555",
    fg="white"
).grid(row=1, column=2, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy,
    width=15,
    bg="#b52b35",
    fg="white"
).grid(row=1, column=3, padx=5, pady=5)


# ==========================================
# 14. START APPLICATION
# ==========================================

root.mainloop()

conn.close()