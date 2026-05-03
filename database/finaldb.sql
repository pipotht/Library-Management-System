CREATE DATABASE LibraryDB;
USE LibraryDB;
CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE Authors (
    AuthorID INT AUTO_INCREMENT PRIMARY KEY,
    AuthorName VARCHAR(100) NOT NULL
);
CREATE TABLE Books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    BookName VARCHAR(255) NOT NULL,
    AuthorID INT NOT NULL,
    PublishYear INT,
    Quantity INT NOT NULL DEFAULT 0,
    CategoryID INT NOT NULL,
    
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        
    CHECK (Quantity >= 0)
);
CREATE TABLE Readers (
    ReaderID INT AUTO_INCREMENT PRIMARY KEY,
    ReaderName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE Borrowing (
    BorrowID INT AUTO_INCREMENT PRIMARY KEY,
    ReaderID INT NOT NULL,
    BookID INT NOT NULL,
    BorrowDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ReturnDate DATETIME,
    Status VARCHAR(20) NOT NULL DEFAULT 'Borrowed',
    
    FOREIGN KEY (ReaderID) REFERENCES Readers(ReaderID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        
    CHECK (Status IN ('Borrowed', 'Returned'))
);
SHOW TABLES;
DESCRIBE Books;

INSERT INTO Categories (CategoryName) VALUES
('Novel'),
('Science'),
('History'),
('Technology'),
('Education'),
('Psychology'),
('Business'),
('Art'),
('Children'),
('Philosophy');

INSERT INTO Authors (AuthorName) VALUES
('Nguyen Nhat Anh'),
('J.K. Rowling'),
('Stephen Hawking'),
('Yuval Noah Harari'),
('Donald Knuth'),
('Dale Carnegie'),
('Robert Kiyosaki'),
('Paulo Coelho'),
('Agatha Christie'),
('Dan Brown');

INSERT INTO Books (BookName, AuthorID, PublishYear, Quantity, CategoryID) VALUES
('Mat Biec', 1, 1990, 10, 1),
('Harry Potter', 2, 1997, 15, 1),
('A Brief History of Time', 3, 1988, 8, 2),
('Sapiens', 4, 2011, 12, 3),
('The Art of Computer Programming', 5, 1968, 5, 4),
('How to Win Friends', 6, 1936, 20, 5),
('Rich Dad Poor Dad', 7, 1997, 18, 7),
('The Alchemist', 8, 1988, 14, 1),
('Murder on the Orient Express', 9, 1934, 9, 1),
('The Da Vinci Code', 10, 2003, 11, 1);

INSERT INTO Readers (ReaderName, Address, PhoneNumber) VALUES
('Tran Van A', 'Hanoi', '0900000001'),
('Le Thi B', 'HCM', '0900000002'),
('Pham Van C', 'Danang', '0900000003'),
('Nguyen Thi D', 'Hue', '0900000004'),
('Hoang Van E', 'Can Tho', '0900000005'),
('Bui Van F', 'Hanoi', '0900000006'),
('Do Thi G', 'HCM', '0900000007'),
('Vu Van H', 'Haiphong', '0900000008'),
('Phan Thi I', 'Quang Ninh', '0900000009'),
('Dang Van K', 'Nghe An', '0900000010');

INSERT INTO Borrowing (ReaderID, BookID, BorrowDate, ReturnDate, Status) VALUES
(1, 1, NOW(), NULL, 'Borrowed'),
(2, 2, NOW(), NULL, 'Borrowed'),
(3, 3, NOW(), NOW(), 'Returned'),
(4, 4, NOW(), NULL, 'Borrowed'),
(5, 5, NOW(), NOW(), 'Returned'),
(6, 6, NOW(), NULL, 'Borrowed'),
(7, 7, NOW(), NOW(), 'Returned'),
(8, 8, NOW(), NULL, 'Borrowed'),
(9, 9, NOW(), NOW(), 'Returned'),
(10, 10, NOW(), NULL, 'Borrowed');

SELECT * FROM Books;
SELECT * FROM Readers;
SELECT * FROM Borrowing;

CREATE INDEX idx_bookname ON Books(BookName);
CREATE INDEX idx_author ON Books(AuthorID);

CREATE VIEW View_BookDetails AS
SELECT 
    b.BookID,
    b.BookName,
    a.AuthorName,
    c.CategoryName,
    b.Quantity
FROM Books b
JOIN Authors a ON b.AuthorID = a.AuthorID
JOIN Categories c ON b.CategoryID = c.CategoryID;

SELECT * FROM View_BookDetails;

CREATE VIEW View_BorrowingReport AS
SELECT 
    r.ReaderName,
    b.BookName,
    br.BorrowDate,
    br.ReturnDate,
    br.Status
FROM Borrowing br
JOIN Readers r ON br.ReaderID = r.ReaderID
JOIN Books b ON br.BookID = b.BookID;

SELECT * FROM View_BorrowingReport;
DELIMITER //

CREATE PROCEDURE BorrowBook(
    IN p_ReaderID INT,
    IN p_BookID INT
)
BEGIN
    DECLARE book_qty INT;

    SELECT Quantity INTO book_qty
    FROM Books
    WHERE BookID = p_BookID;

    IF book_qty > 0 THEN
        INSERT INTO Borrowing (ReaderID, BookID, BorrowDate, Status)
        VALUES (p_ReaderID, p_BookID, NOW(), 'Borrowed');
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book is out of stock';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ReturnBook(
    IN p_BorrowID INT
)
BEGIN
    UPDATE Borrowing
    SET Status = 'Returned',
        ReturnDate = NOW()
    WHERE BorrowID = p_BorrowID;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_reduce_quantity
AFTER INSERT ON Borrowing
FOR EACH ROW
BEGIN
    UPDATE Books
    SET Quantity = Quantity - 1
    WHERE BookID = NEW.BookID;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_increase_quantity
AFTER UPDATE ON Borrowing
FOR EACH ROW
BEGIN
    IF NEW.Status = 'Returned' THEN
        UPDATE Books
        SET Quantity = Quantity + 1
        WHERE BookID = NEW.BookID;
    END IF;
END //

DELIMITER ;

SELECT BookID, Quantity FROM Books WHERE BookID = 1;
CALL BorrowBook(2, 1);
SELECT BookID, Quantity FROM Books WHERE BookID = 1;
CALL ReturnBook(1);
SELECT BookID, Quantity FROM Books WHERE BookID = 1;
SHOW INDEX FROM Books;

DELIMITER //
CREATE FUNCTION fn_DaysOverdue(p_BorrowID INT)
RETURNS INT
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE borrow_dt DATETIME;
    DECLARE days_diff INT;

    SELECT BorrowDate INTO borrow_dt
    FROM Borrowing
    WHERE BorrowID = p_BorrowID AND Status = 'Borrowed';

    IF borrow_dt IS NULL THEN
        RETURN 0;
    END IF;

    SET days_diff = DATEDIFF(NOW(), borrow_dt);
    RETURN days_diff;
END //
DELIMITER ;

CREATE VIEW View_OverdueReport AS
SELECT
    r.ReaderName,
    b.BookName,
    br.BorrowDate,
    fn_DaysOverdue(br.BorrowID) AS DaysOverdue
FROM Borrowing br
JOIN Readers r ON br.ReaderID = r.ReaderID
JOIN Books   b ON br.BookID   = b.BookID
WHERE br.Status = 'Borrowed'
  AND fn_DaysOverdue(br.BorrowID) > 7;

UPDATE Borrowing SET BorrowDate = NOW() - INTERVAL 10 DAY WHERE BorrowID = 1;
UPDATE Borrowing SET BorrowDate = NOW() - INTERVAL 15 DAY WHERE BorrowID = 4;
UPDATE Borrowing SET BorrowDate = NOW() - INTERVAL  8 DAY WHERE BorrowID = 6;

SELECT * FROM View_OverdueReport;
SELECT fn_DaysOverdue(1);