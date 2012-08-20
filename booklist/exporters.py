from booklist.gbook_search import get_isbn
from collections import OrderedDict


def make_row(book):
    """Returns and OrderedDict of the information required by the goodreads
    csv format.

    """
    row = OrderedDict()
    row["title"] = '"' + book.title + '"'

    row["authors"] = " and ".join([author.first_name + ' ' + author.last_name\
                                   for author in book.authors])
    row["isbn"] = get_isbn(book)
    row["my rating"] = ""
    row["average rating"] = ""
    row["publisher"] = ""
    row["binding"] = ""
    row["year published"] = ""
    row["original publication year"] = ""
    row["date read"] = ""
    row["date added"] = ""
    row["bookshelves"] = ""
    row["my review"] = ""
    return row


def export_goodreads(b_list, output_file):
    """Exports a book list to a csv file suitable for uploading to 
    goodreads.com.

    """
    with open(output_file, "w") as f:
        print(("Title, Author, ISBN, My Rating, Average Rating, Publisher, "
               "Binding, Year Published, Original Publication Year, "
               "Date Read, Date Added, Bookshelves, My Review"), file=f)

        for book in b_list.reading_now:
            row = make_row(book)
            row["bookshelves"] = "reading-now"
            print(", ".join(row.values()), file=f)

        for book in b_list.to_read:
            row = make_row(book)
            row["bookshelves"] = "to-read"
            print(", ".join(row.values()), file=f)

        for book in b_list.get_previously_read_books():
            row = make_row(book)
            row["bookshelves"] = "read"
            date = b_list.date_read(book)
            row["date read"] = "/".join([str(x) for x in 
                                        [date.month, date.day, date.year]])
            row["my review"] = '"' + b_list.comments(book).replace("\n"," ")\
                                   + '"'
            print(", ".join(row.values()), file=f)
