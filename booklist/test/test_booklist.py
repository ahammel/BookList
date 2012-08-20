import pytest
from booklist import parsers, exporters, gbook_search
from datetime import date
import os


class SetupParserTests(object):
    blist_file = "test/books.txt"
    blist = parsers.read_book_list(blist_file)

    brin = parsers.Author("David", "Brin")
    benford = parsers.Author("Gregory", "Benford")
    vinge = parsers.Author("Vernor", "Vinge")
    abe = parsers.Author("Kōbō", "Abe")
    gibson = parsers.Author("William", "Gibson")

    heart_of_the_comet = parsers.Book("Heart of the Comet",
                                      [benford, brin])
    a_fire_upon_the_deep = parsers.Book("A Fire Upon the Deep",
                                        [vinge])
    the_woman_in_the_dunes = parsers.Book("The Woman in the Dunes",
                                          [abe])
    spook_country = parsers.Book("Spook Country", [gibson])


class TestParserFunctions(SetupParserTests):
    def test_parse_book(self):
        assert parsers.parse_book("Heart of the Comet; Benford, Gregory "
                                  "& Brin, David\n") == self.heart_of_the_comet
        with pytest.raises(parsers.ImproperFormattingError):
            parsers.parse_book("some line of text that is not a book title")
        with pytest.raises(parsers.ImproperFormattingError):
            parsers.parse_book("some text; with a semicolon")
        with pytest.raises(parsers.ImproperFormattingError):
            parsers.parse_book("some text; with a semicolon, and, some commas")

    def test_read_book_list(self):
        assert self.blist.reading_now == [self.heart_of_the_comet]
        
        for book in [self.a_fire_upon_the_deep, self.the_woman_in_the_dunes]:
            assert book in self.blist.to_read

        assert self.blist.priority == [self.a_fire_upon_the_deep]

        assert self.blist.get_previously_read_books() == [self.spook_country]

        assert self.blist.date_read(self.spook_country) == date(2012, 6, 23)

        assert self.blist.comments(self.spook_country) ==\
                                 ("Weaker than Patten Recognition, but still "
                                  "quite readable. And hey: parkour\n"
                                  "chace scene!  Hopefully Zero History will "
                                  "be a stronger finish.")

class SetupGBookSearchTest(SetupParserTests):
    pass

class TestGbookSearchFunctions(SetupGBookSearchTest):
    def test_get_isbn(self):
        isbn = gbook_search.get_isbn(self.spook_country)
        assert isbn == "9780425226711"


class SetupExportersTest(SetupParserTests):
    pass


class TestExportersFunctions(SetupExportersTest):
    def test_export_goodreads(self):
        exporters.export_goodreads(self.blist, "gr_test.csv")
        with open("gr_test.csv") as f:
            test_lines = f.readlines()
        with open("test/books.csv") as f:
            known_lines = f.readlines()
        assert test_lines == known_lines
        os.remove("gr_test.csv")
        
