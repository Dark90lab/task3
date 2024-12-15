from project.books.models import Book
import pytest
from sqlalchemy.exc import DataError


# Correct Input Tests

@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe",
     "Gabriel García Márquez, Nobel Laureate and Renowned Latin American Author", 1999, "Historical Fiction", "available"),
    ("Hello", "Author", 2000, "Action", "available"),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction", "Available"),
    ("A Brief History of Time", "Stephen Hawking", 1988, "Science", "Checked Out"),
    ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction", "Available"),
    ("1984", "George Orwell", 1949, "Dystopian", "Reserved"),
    ("The Art of War", "Sun Tzu", -500, "Philosophy", "Available"),
])
def test_correct_input(name, author, year_published, book_type, status):
    book = Book(name=name, author=author,
                year_published=year_published, book_type=book_type, status=status)

    assert book.name == name
    assert book.author == author
    assert book.year_published == year_published
    assert book.book_type == book_type
    assert book.status == status

# Input Tests Boundaries


@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("H"*64, "A"*64, 2000, "A"*20, "a"*20),
])
def test_correct_input_boundaries(name, author, year_published, book_type, status):
    book = Book(name=name, author=author,
                year_published=year_published, book_type=book_type, status=status)

    assert book.name == name
    assert book.author == author
    assert book.year_published == year_published
    assert book.book_type == book_type
    assert book.status == status

# Incorrect Inputs Tests


@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("", "F. Scott Fitzgerald", 1925, "Fiction", "Available"),
    (None, "F. Scott Fitzgerald", 1925, "Fiction", "Available"),
    ("A"*65, "F. Scott Fitzgerald", 1925, "Fiction", "Available"),
    ("A Brief History of Time", "", 1988, "Science", "Checked Out"),
    ("A Brief History of Time", None, 1988, "Science", "Checked Out"),
    ("A Brief History of Time", "A"*65, 1988, "Science", "Checked Out"),
    ("To Kill a Mockingbird", "Harper Lee", -500, "Fiction", "Available"),
    ("1984", "George Orwell", 1949, "Dystopian", ""),
    ("1984", "George Orwell", 1949, "Dystopian", None),
    ("1984", "George Orwell", 1949, "Dystopian", "A"*21),
    ("The Art of War", "Sun Tzu", 1500, "", "Available"),
    ("The Art of War", "Sun Tzu", 1500, None, "Available"),
    ("The Art of War", "Sun Tzu", 1500, "A"*21, "Available"),
    (None, None, None, None, None)
])
def test_invalid_input(name, author, year_published, book_type, status):
    with pytest.raises(DataError):
        Book(name=name, author=author,
             year_published=year_published, book_type=book_type, status=status)


# Extreme Input Tests

@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("H"*1000, "A"*1000, 2000, "A"*1000, "a"*1000),
    ("H"*1000, "A"*10000, 20000, "A"*10000, "a"*10000),
    ("H"*41000, "A"*400000, 420000, "A"*410000, "a"*410000)
])
def test_extreme_inputs(name, author, year_published, book_type, status):
    with pytest.raises(DataError):
        Book(name=name, author=author,
             year_published=year_published, book_type=book_type, status=status)


# XSS Tests
@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("\"-prompt(8)-\"", "Author", 1988, "Science", "Checked Out"),
    ("'-prompt(8)-'", "Author", 1988, "Science", "Checked Out"),
    ("'-prompt(8)-'", "Author", 1988, "Science", "Checked Out"),
    ("<img/src/onerror=prompt(8)/>", "Author", 1988, "Science", "Checked Out")
    ("<script src=1 href=1 onerror=\"javascript:alert(1)\"></script>",
     "Author", 1988, "Science", "Checked Out")
    # etc. same for each string filed
])
def test_xss_inputs(name, author, year_published, book_type, status):
    with pytest.raises(DataError):
        Book(name=name, author=author,
             year_published=year_published, book_type=book_type, status=status)

# SQL Injection Tests


@pytest.mark.parametrize("name, author, year_published, book_type,status", [
    ("-- or # ", "Author", 1988, "Science", "Checked Out"),
    ("\" OR 1 = 1 -- - ", "Author", 1988, "Science", "Checked Out"),
    ("``````````UNION SELECT '2'", "Author", 1988, "Science", "Checked Out"),
    ("'1' ORDER BY 1--+", "Author", 1988, "Science", "Checked Out")
    # etc. same for each string filed
])
def test_sql_inputs(name, author, year_published, book_type, status):
    with pytest.raises(DataError):
        Book(name=name, author=author,
             year_published=year_published, book_type=book_type, status=status)
