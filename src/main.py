import mysql.connector
from tabulate import tabulate

# ===== CONNECT =====
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1511",
    database="LibraryDB"  
)
cursor = conn.cursor()

print("✅ Connected to LibraryDB!")

# =========================
# ===== BOOK =============
# =========================

def view_books():
    cursor.execute("""
        SELECT b.BookID, b.BookName,
               CONCAT(a.AuthorID, ' - ', a.AuthorName),
               b.PublishYear, b.Quantity,
               CONCAT(c.CategoryID, ' - ', c.CategoryName)
        FROM Books b
        JOIN Authors a ON b.AuthorID = a.AuthorID
        JOIN Categories c ON b.CategoryID = c.CategoryID
    """)
    rows = cursor.fetchall()

    print(tabulate(rows,
        headers=["ID","Name","Author","Year","Qty","Category"],
        tablefmt="fancy_grid"))

def add_book():
    name = input("Book name: ")
    author = input("Author ID: ")
    year = input("Year: ")
    qty = input("Quantity: ")
    cat = input("Category ID: ")

    # lấy info để hiển thị
    cursor.execute("SELECT AuthorName FROM Authors WHERE AuthorID=%s", (author,))
    author_name = cursor.fetchone()

    cursor.execute("SELECT CategoryName FROM Categories WHERE CategoryID=%s", (cat,))
    cat_name = cursor.fetchone()

    print("\n===== CONFIRM ADD BOOK =====")
    print(f"Name: {name}")
    print(f"Author: {author} - {author_name[0] if author_name else 'Unknown'}")
    print(f"Year: {year}")
    print(f"Quantity: {qty}")
    print(f"Category: {cat} - {cat_name[0] if cat_name else 'Unknown'}")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("""
        INSERT INTO Books (BookName, AuthorID, PublishYear, Quantity, CategoryID)
        VALUES (%s,%s,%s,%s,%s)
    """, (name, author, year, qty, cat))
    conn.commit()

    print(f"✅ Book added! ID = {cursor.lastrowid}")

def edit_book():
    book_id = input("Book ID: ")
    qty = input("New quantity: ")

    cursor.execute("UPDATE Books SET Quantity=%s WHERE BookID=%s", (qty, book_id))
    conn.commit()

    print("✅ Book updated!")

def delete_book():
    book_id = input("Book ID: ")

    cursor.execute("""
        SELECT BookName FROM Books WHERE BookID=%s
    """, (book_id,))
    book = cursor.fetchone()

    if not book:
        print("❌ Book not found!")
        return

    print("\n===== CONFIRM DELETE BOOK =====")
    print(f"Book: {book[0]} (ID: {book_id})")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("DELETE FROM Books WHERE BookID=%s", (book_id,))
    conn.commit()

    print("✅ Deleted!")

def search_book():
    keyword = input("Search name: ")

    cursor.execute("""
        SELECT b.BookID, b.BookName,
               CONCAT(a.AuthorID, ' - ', a.AuthorName),
               b.PublishYear, b.Quantity,
               CONCAT(c.CategoryID, ' - ', c.CategoryName)
        FROM Books b
        JOIN Authors a ON b.AuthorID = a.AuthorID
        JOIN Categories c ON b.CategoryID = c.CategoryID
        WHERE b.BookName LIKE %s
    """, ("%" + keyword + "%",))

    rows = cursor.fetchall()

    print(tabulate(rows,
        headers=["ID","Name","Author","Year","Qty","Category"],
        tablefmt="fancy_grid"))

# =========================
# ===== READER ============
# =========================
def view_reader():
    cursor.execute("SELECT * FROM Readers")
    rows = cursor.fetchall()
    print(tabulate(rows,
        headers=["ID","Name","Address","Phone"],
        tablefmt="fancy_grid"))

def add_reader():
    name = input("Name: ")
    address = input("Address: ")
    phone = input("Phone: ")

    print("\n===== CONFIRM ADD READER =====")
    print(f"Name: {name}")
    print(f"Address: {address}")
    print(f"Phone: {phone}")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("""
        INSERT INTO Readers (ReaderName, Address, PhoneNumber)
        VALUES (%s,%s,%s)
    """, (name, address, phone))
    conn.commit()

    print(f"✅ Reader added! ID = {cursor.lastrowid}")

def update_reader():
    rid = input("Reader ID: ")
    address = input("New address: ")
    phone = input("New phone: ")

    cursor.execute("""
        UPDATE Readers
        SET Address=%s, PhoneNumber=%s
        WHERE ReaderID=%s
    """, (address, phone, rid))

    conn.commit()
    print("✅ Reader updated!")

# =========================
# ===== AUTHOR ============
# =========================

def view_authors():
    cursor.execute("SELECT * FROM Authors")
    rows = cursor.fetchall()

    print(tabulate(rows, headers=["ID","Author"], tablefmt="fancy_grid"))

def add_author():
    name = input("Author name: ")

    print("\n===== CONFIRM ADD AUTHOR =====")
    print(f"Author: {name}")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("INSERT INTO Authors (AuthorName) VALUES (%s)", (name,))
    conn.commit()

    print(f"✅ Author added! ID = {cursor.lastrowid}")

def delete_author():
    aid = input("Author ID: ")

    cursor.execute("SELECT AuthorName FROM Authors WHERE AuthorID=%s", (aid,))
    author = cursor.fetchone()

    if not author:
        print("❌ Not found!")
        return

    print("\n===== CONFIRM DELETE AUTHOR =====")
    print(f"Author: {author[0]} (ID: {aid})")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("DELETE FROM Authors WHERE AuthorID=%s", (aid,))
    conn.commit()

    print("✅ Deleted!")

# =========================
# ===== CATEGORY ==========
# =========================

def view_categories():
    cursor.execute("SELECT * FROM Categories")
    rows = cursor.fetchall()

    print(tabulate(rows, headers=["ID","Category"], tablefmt="fancy_grid"))

def add_category():
    name = input("Category name: ")

    print("\n===== CONFIRM ADD CATEGORY =====")
    print(f"Category: {name}")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("INSERT INTO Categories (CategoryName) VALUES (%s)", (name,))
    conn.commit()

    print(f"✅ Category added! ID = {cursor.lastrowid}")

def delete_category():
    cid = input("Category ID: ")

    cursor.execute("SELECT CategoryName FROM Categories WHERE CategoryID=%s", (cid,))
    cat = cursor.fetchone()

    if not cat:
        print("❌ Not found!")
        return

    print("\n===== CONFIRM DELETE CATEGORY =====")
    print(f"Category: {cat[0]} (ID: {cid})")

    confirm = input("Confirm? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.execute("DELETE FROM Categories WHERE CategoryID=%s", (cid,))
    conn.commit()

    print("✅ Deleted!")

# =========================
# ===== BORROW ============
# =========================

def borrow_book():
    rid = input("Enter Reader ID: ")
    bid = input("Enter Book ID: ")

    # Lấy thông tin reader
    cursor.execute("SELECT ReaderName FROM Readers WHERE ReaderID=%s", (rid,))
    reader = cursor.fetchone()

    # Lấy thông tin book
    cursor.execute("""
        SELECT b.BookName, b.Quantity, a.AuthorName
        FROM Books b
        JOIN Authors a ON b.AuthorID = a.AuthorID
        WHERE b.BookID=%s
    """, (bid,))
    book = cursor.fetchone()

    if not reader or not book:
        print("❌ Invalid Reader ID or Book ID!")
        return

    print("\n===== CONFIRM BORROW =====")
    print(f"Reader: {reader[0]} (ID: {rid})")
    print(f"Book: {book[0]} (Author: {book[2]})")
    print(f"Available Quantity: {book[1]}")
    print("⚠️ Note: Borrow duration is 7 days")

    confirm = input("Confirm borrow? (y/n): ").lower()

    if confirm != 'y':
        print("❌ Cancelled!")
        return

    try:
        cursor.callproc("BorrowBook", [rid, bid])
        conn.commit()

        cursor.execute("SELECT MAX(BorrowID) FROM Borrowing")
        borrow_id = cursor.fetchone()[0]

        print(f"✅ Borrow successful! Borrow ID = {borrow_id}")

    except Exception as e:
        print("❌", e)
        
# =========================
# ===== RETURN ============
# =========================    

def return_book():
    borrow_id = input("Enter Borrow ID: ")

    cursor.execute("""
    SELECT br.BorrowID, r.ReaderName, b.BookName,
           br.BorrowDate, br.Status
    FROM Borrowing br
    JOIN Readers r ON br.ReaderID = r.ReaderID
    JOIN Books b ON br.BookID = b.BookID
    WHERE br.BorrowID=%s
""", (borrow_id,))

    data = cursor.fetchone()

    if not data:
        print("❌ Invalid Borrow ID!")
        return
    
    if data[4] == 'Returned':
        print("⚠️ This book has already been returned!")
        return

    from datetime import datetime

    borrow_date = data[3]
    today = datetime.now()
    days = (today - borrow_date).days

    print("\n===== CONFIRM RETURN =====")
    print(f"Borrow ID: {data[0]}")
    print(f"Reader: {data[1]}")
    print(f"Book: {data[2]}")
    print(f"Borrow Date: {borrow_date}")
    print(f"Days Borrowed: {days}")

    if days > 7:
        print("⚠️ OVERDUE! Late return!")

    confirm = input("Confirm return? (y/n): ").lower()

    if confirm != 'y':
        print("❌ Cancelled!")
        return

    cursor.callproc("ReturnBook", [borrow_id])
    conn.commit()

    print("✅ Return successful!")

def overdue_with_udf():
    cursor.execute("""
        SELECT r.ReaderName, b.BookName,
               br.BorrowDate,
               fn_DaysOverdue(br.BorrowID) AS DaysOverdue
        FROM Borrowing br
        JOIN Readers r ON br.ReaderID = r.ReaderID
        JOIN Books b ON br.BookID = b.BookID
        WHERE br.Status = 'Borrowed'
        AND fn_DaysOverdue(br.BorrowID) > 7
        ORDER BY DaysOverdue DESC
    """)
    rows = cursor.fetchall()
    print(tabulate(rows,
        headers=["Reader","Book","BorrowDate","Days Overdue"],
        tablefmt="fancy_grid"))
    
# =========================
# ===== REPORT ============
# =========================

def report():
    cursor.execute("""
        SELECT br.BorrowID,
               r.ReaderName,
               b.BookName,
               br.BorrowDate,
               br.ReturnDate,
               br.Status
        FROM Borrowing br
        JOIN Readers r ON br.ReaderID = r.ReaderID
        JOIN Books b ON br.BookID = b.BookID
    """)
    rows = cursor.fetchall()

    print(tabulate(rows,
        headers=["BorrowID","Reader","Book","BorrowDate","ReturnDate","Status"],
        tablefmt="fancy_grid"))

def stats():
    cursor.execute("SELECT COUNT(*) FROM Books")
    b = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Readers")
    r = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Borrowing")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Borrowing WHERE Status='Borrowed'")
    borrowing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Borrowing WHERE Status='Returned'")
    returned = cursor.fetchone()[0]

    print("\n📊 STATISTICS")
    print(f"Total Books: {b}")
    print(f"Total Readers: {r}")
    print(f"Total Borrow Records: {total}")
    print(f"Currently Borrowing: {borrowing}")
    print(f"Returned: {returned}")

def top_books():
    cursor.execute("""
        SELECT b.BookName, COUNT(*) as TotalBorrow
        FROM Borrowing br
        JOIN Books b ON br.BookID = b.BookID
        GROUP BY b.BookName
        ORDER BY TotalBorrow DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()

    print(tabulate(rows,
        headers=["Book","Times Borrowed"],
        tablefmt="fancy_grid"))

# =========================
# ===== MENUS ============
# =========================

def book_menu():
    while True:
        print("\n--- BOOK MANAGEMENT ---")
        print("1. View")
        print("2. Add")
        print("3. Edit")
        print("4. Delete")
        print("5. Search")
        print("6. Back")

        c = input("Choose: ")
        if c == "1": view_books()
        elif c == "2": add_book()
        elif c == "3": edit_book()
        elif c == "4": delete_book()
        elif c == "5": search_book()
        elif c == "6": break

def reader_menu():
    while True:
        print("\n--- READER MANAGEMENT ---")
        print("1. View Reader")
        print("2. Add Reader")
        print("3. Update Reader")
        print("4. Back")

        c = input("Choose: ")
        if c == "1": view_reader()
        elif c == "2": add_reader()
        elif c == "3": update_reader()
        elif c == "4": break

def author_menu():
    while True:
        print("\n--- AUTHOR MANAGEMENT ---")
        print("1. View Authors")
        print("2. Add Author")
        print("3. Delete Author")
        print("4. Back")

        c = input("Choose: ")
        if c == "1": view_authors()
        elif c == "2": add_author()
        elif c == "3": delete_author()
        elif c == "4": break

def category_menu():
    while True:
        print("\n--- CATEGORY MANAGEMENT ---")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Delete Category")
        print("4. Back")

        c = input("Choose: ")
        if c == "1": view_categories()
        elif c == "2": add_category()
        elif c == "3": delete_category()
        elif c == "4": break

def borrow_menu():
    while True:
        print("\n--- BORROW / RETURN ---")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Back")

        c = input("Choose: ")
        if c == "1": borrow_book()
        elif c == "2": return_book()
        elif c == "3": break

def report_menu():
    while True:
        print("\n--- REPORTS ---")
        print("1. Borrow Details")
        print("2. Overdue")
        print("3. Statistics")
        print("4. Top Books")
        print("5. Back")

        c = input("Choose: ")
        if c == "1": report()
        elif c == "2": overdue_with_udf()
        elif c == "3": stats()
        elif c == "4": top_books()
        elif c == "5": break

# =========================
# ===== MAIN ============
# =========================

while True:
    print("\n========= LIBRARY SYSTEM =========")
    print("1. Book Management")
    print("2. Reader Management")
    print("3. Author Management")
    print("4. Category Management")
    print("5. Borrow / Return")
    print("6. Reports")
    print("7. Exit")

    c = input("Choose: ")

    if c == "1": book_menu()
    elif c == "2": reader_menu()
    elif c == "3": author_menu()
    elif c == "4": category_menu()
    elif c == "5": borrow_menu()
    elif c == "6": report_menu()
    elif c == "7":
        print("👋 Goodbye!")
        break