import unittest
from library import Library
from book import Book
from member import Member

class TestLibrarySystem(unittest.TestCase):

    def test_complete_borrow_and_return_lifecycle(self):
        library = Library()
        book = Book("B02", "Dune")
        member = Member("M02", "Charlie")

        # 1. Charlie borrows Dune
        library.issue_book(member, book)
        self.assertIn("Dune", member.list_borrowed())

        # 2. Charlie tries to borrow it again (Should fail)
        with self.assertRaises(ValueError):
            library.issue_book(member, book)

        # 3. Charlie returns Dune safely
        library.receive_book(member, book)
        self.assertTrue(book.is_available)
        self.assertEqual(len(member.list_borrowed()), 0)

if __name__ == "__main__":
    unittest.main()