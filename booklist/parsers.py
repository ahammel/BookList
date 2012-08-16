from collections import namedtuple
from datetime import date


MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}


class UnreadBookError(KeyError):
    """The exception raised when a function which assumes a read book is
    passed an unread book.

    """


class ImproperFormattingError(ValueError):
    """The exception raised when trying to parse and imporperly formatted 
    line.

    """


Author = namedtuple("Author", "first_name, last_name")


Book = namedtuple("Book", "title, authors")


class BookList(object):
    def __init__(self):
        self.reading_now = []
        self.to_read = []
        self.priority = []
        self.previously_read_data = []

    def get_previously_read_books(self):
        return [book for book, date, comments in self.previously_read_data]

    def date_read(self, book):
        for item, date, notes in self.previously_read_data:
            if item == book:
                date_read = date
                break
        else:
            raise UnreadBookError("This book has not been previously read")

        return date_read

    def comments(self, book):
        for item, date, notes in self.previously_read_data:
            if item == book:
                comments = notes
                break
        else:
            raise UnreadBookError("This book has not been previously read")

        return comments


def parse_book(line):
    """Given a line of text, returns a book object using information found in
    that line, or raises an ImproperFormattingError if the line is not
    a properly formatted book title.

    """
    try:
        title_text, author_text = line.split(";")
    except ValueError:
        raise ImproperFormattingError(line)

    title = title_text.strip()
    authors = []

    for author in author_text.split("&"):
        authors.append(tuple(author.split(",")))

    try:
        authors = [Author(first.strip(), last.strip()) for last, first in authors]
    except ValueError:
        raise ImproperFormattingError(line)

    return Book(title, authors)


def parse_books_reading_now(book_list, file_stream):
    """Given a book list and a file stream, adds the books found in the stream
    to the reading_now list of the book_list. Breaks when it encounters the line
          "---\n"

    """
    for line in file_stream:
        if line == "---\n":
            break
        try:
            book = parse_book(line)
            book_list.reading_now.append(book)
        except ImproperFormattingError:
            pass


def parse_priority_books(book_list, file_stream):
    """Given a book list and a file stream, adds the books found in the stream
    to the priority list of the book_list. Breaks when it encounters the line
          "---\n"

    """
    for line in file_stream:
        if line == "---\n":
            break
        try:
            book = parse_book(line)
            book_list.priority.append(book)
            book_list.to_read.append(book)
        except ImproperFormattingError:
            pass


def parse_books_to_read(book_list, file_stream):
    """Given a book list and a file stream, adds the books found in the stream
    to the to_read list of the book_list. Breaks when it encounters the line
          "Completed:\n"

    """
    for line in file_stream:
        if line == "Completed:\n":
            break
        try:
            book = parse_book(line)
            book_list.to_read.append(book)
        except ImproperFormattingError:
            pass


def parse_previously_read_books(book_list, file_stream):
    """Given a book list and a file stream, adds the books found in the stream
    to the to_read list of the book_list, along with the date read and any 
    comments.

    """
    date_read = None
    comment_list = []
    for line in file_stream:
        if line[:3] in MONTHS and not date_read:
            date_read = parse_date(line)
        elif line[:3] in MONTHS:
            comments = "".join(comment_list).strip()
            data = (book, date_read, comments)
            book_list.previously_read_data.append(data)
            date = parse_date(line)
            comment_list = []
        else:
            try:
                book = parse_book(line)
            except ImproperFormattingError:
                comment_list.append(line)
    
    comments = "".join(comment_list).strip()
    data = (book, date_read, comments)
    book_list.previously_read_data.append(data)


def parse_date(line):
    """Returns a datetime.date from a line of the format 'Mon DD, YYYY'"""
    month = MONTHS[line[:3]]
    day = int(line[4:6])
    year = int(line[8:12])
    return date(year, month, day)


def read_book_list(book_list_file):
    """Returns a BookList object from a properly-formatted text file."""
    blist = BookList()
    
    with open(book_list_file) as f:
        parse_books_reading_now(blist, f)
        parse_priority_books(blist, f)
        parse_books_to_read(blist, f)
        parse_previously_read_books(blist, f)
    
    return blist
