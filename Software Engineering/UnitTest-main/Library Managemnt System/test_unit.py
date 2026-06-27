import unittest
from book import Book
from member import Member

class TestLibraryUnit(unittest.TestCase):

    def setUp(self):
        self.book = Book("B01", "The Hobbit")
        self.member = Member("M01", "Alice")

    def test_book_borrow_and_return(self):
        self.assertTrue(self.book.borrow_book())
        self.assertFalse(self.book.is_available)
        
        self.assertTrue(self.book.return_book())
        self.assertTrue(self.book.is_available)

    def test_member_book_tracking(self):
        self.member.add_book("The Hobbit")
        self.assertIn("The Hobbit", self.member.list_borrowed())
        
        self.member.remove_book("The Hobbit")
        self.assertEqual(len(self.member.list_borrowed()), 0)

    def test_invalid_return(self):
        with self.assertRaises(ValueError):
            self.book.return_book()

if __name__ == "__main__":
    unittest.main()