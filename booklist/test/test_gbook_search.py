from booklist import gbook_search, parsers

class SetupGBookSearchTest(object):
    gibson = parsers.Author("William", "Gibson")
    spook_country = parsers.Book("Spook Country", [gibson])

class TestGbookSearchFunctions(SetupGBookSearchTest):
    def test_get_isbn(self):
        isbn = gbook_search.get_isbn(self.spook_country)
        assert isbn == "9780425226711"
