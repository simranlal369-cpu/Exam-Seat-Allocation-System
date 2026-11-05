# 🎓 Exam Seat Allocation System

## 📌 Project Overview

The **Exam Seat Allocation System** is a Python-based desktop application developed using **Tkinter and SQLite**. It is designed to simplify and automate the process of allocating examination seats to students.

The system allows administrators to add student details, manage examination rooms, automatically generate randomized seat allocations, and view or search student seating information.

The project aims to reduce manual effort, save time, minimize allocation errors, and make examination seat management more organized and efficient.

## 🚀 Features

- **Add Student:** Register students using their roll number, name, and course.
- **Add Examination Room:** Add rooms along with their seating capacities.
- **View Students:** Display all registered students.
- **Automatic Seat Allocation:** Randomly allocate seats to students based on available room capacity.
- **View Allocations:** Display the allocated room and seat number of each student.
- **Search Student:** Search for a student using their roll number.
- **Clear Table:** Clear the displayed records.
- **Database Management:** Store student, room, and allocation details using SQLite.
- **Input Validation:** Prevent duplicate roll numbers, duplicate room numbers, and invalid room capacities.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical User Interface (GUI) |
| SQLite3 | Database management |
| Random Module | Randomized seat allocation |
| ttk (Treeview) | Displaying student and allocation records |

## 📂 Project Structure

```text
Exam-Seat-Allocation-System/
│
├── main.py
│
├── exam_seating.db
│
└── README.md
```

**Note:** The `exam_seating.db` database file is automatically created when the application runs for the first time.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Exam-Seat-Allocation-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Exam-Seat-Allocation-System
```

### 3. Run the Application

```bash
python exam_seat_allocation_refined.py
```

<img width="1307" height="980" alt="image" src="https://github.com/user-attachments/assets/c1ebd5ba-1a23-404f-9bbe-821b9e77ee98" />

### 4. Start Using the Application

- Add student information.
- Add examination rooms and their capacities.
- Click **Allocate Seats** to generate random seating arrangements.
- View or search student allocation details.

## 🗄️ Database Design

The application uses SQLite with three main tables:

### 1. Students Table

Stores student information.

- `roll_no` – Student's unique roll number.
- `name` – Student's name.
- `course` – Student's course.

### 2. Rooms Table

Stores examination room information.

- `room_no` – Unique room number.
- `capacity` – Maximum number of students the room can accommodate.

### 3. Allocations Table

Stores the generated seating arrangements.

- `roll_no` – Student's roll number.
- `room_no` – Assigned examination room.
- `seat_no` – Assigned seat number.

## 👥 Team Members

This project was developed collaboratively by:

1. **Simran Lal**
2. **Riaz Mondal**
3. **Koyel Manna**
4. **Gunjan Dey**
5. **Arpita Panda**

## 🎯 Project Objective

The primary objective of this project is to develop a simple, user-friendly, and efficient examination seat allocation system that automates student seating arrangements while maintaining organized records through a database.

## 🔮 Future Enhancements

- Generate downloadable seating arrangement reports in PDF format.
- Add administrator login and authentication.
- Support editing and deleting student and room records.
- Display room-wise seating arrangements.
- Export student allocation details to Excel.
- Improve the allocation algorithm to support additional examination seating rules.

## 📜 License

This project is developed for educational and academic purposes.

---

**Developed with Python ❤️ by Team Exam Seat Allocation System.**
