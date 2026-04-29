# 📚 Library Management System

A console-based Library Management System developed using **MySQL** and **Python** as the final project for the *Introduction to Databases* course at National Economics University.

---

## 🗂 Project Structure

```
Library-Management-System/
├── database/
│   └── finaldb.sql
├── src/
│   └── main.py
├── docs/
│   └── screenshots/
└── README.md
```

---

## ⚙️ Requirements

### Database

* MySQL 8.x
* MySQL Workbench (recommended)

### Python

* Python 3.x
* mysql-connector-python
* tabulate

Install dependencies:

```bash
pip install mysql-connector-python tabulate
```

---

## 🚀 Setup & Run

### Step 1 — Import Database

Open MySQL Workbench, load `finaldb.sql`, and execute the script.
This will create the `LibraryDB` database with all required tables, views, stored procedures, triggers, and sample data.

### Step 2 — Configure Connection

Edit database credentials in `main.py`:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="LibraryDB"
)
```

### Step 3 — Run Application

```bash
python src/main.py
```

---

## 🗄 Database Schema

| Table      | Description                                                       |
| ---------- | ----------------------------------------------------------------- |
| Books      | Stores book information (title, author, year, quantity, category) |
| Authors    | Author records                                                    |
| Categories | Book classification                                               |
| Readers    | Library members                                                   |
| Borrowing  | Borrow and return transactions                                    |

### Advanced Database Features

* Indexes: `idx_bookname`, `idx_author`
* Views: `View_BookDetails`, `View_BorrowingReport`, `View_OverdueReport`
* Stored Procedures: `BorrowBook`, `ReturnBook`
* Triggers: `trg_reduce_quantity`, `trg_increase_quantity`
* User-Defined Function: `fn_DaysOverdue`

---

## 🖥 Application Features

* **Book Management:** View, add, edit, delete, and search books
* **Reader Management:** Register and update reader information
* **Author Management:** View, add, and delete authors
* **Category Management:** Manage book categories
* **Borrow & Return System:** Process borrowing and returning with validation
* **Reports:** Borrow history, overdue tracking, statistics, and top books

### Key Behaviors

* Borrowing is validated via stored procedures (prevents out-of-stock)
* Returning detects overdue cases (> 7 days)
* Prevents duplicate returns
* Book quantity is automatically updated via triggers

---

## 🛠 Tech Stack

| Component     | Technology             |
| ------------- | ---------------------- |
| Database      | MySQL 8.x              |
| Programming   | Python 3.x             |
| Connector     | mysql-connector-python |
| Output Format | tabulate               |

---

## 👤 Author

**Bui Vi Anh**
Student ID: 11247122
Class: DS66B
National Economics University — College of Technology
Course: Introduction to Databases