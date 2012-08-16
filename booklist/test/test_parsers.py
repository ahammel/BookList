import pytest
from booklist import parsers
from datetime import date


class SetupParserTests(object):
    blist_file = "test/books.txt"

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
        blist = parsers.read_book_list(self.blist_file)

        assert blist.reading_now == [self.heart_of_the_comet]
        
        for book in [self.a_fire_upon_the_deep, self.the_woman_in_the_dunes]:
            assert book in blist.to_read

        assert blist.priority == [self.a_fire_upon_the_deep]

        assert blist.get_previously_read_books() == [self.spook_country]

        assert blist.date_read(self.spook_country) == date(2012, 6, 23)

        assert blist.comments(self.spook_country) ==\
                                 ("Weaker than Patten Recognition, but still "
                                  "quite readable. And hey: parkour\n"
                                  "chace scene!  Hopefully Zero History will "
                                  "be a stronger finish.")
