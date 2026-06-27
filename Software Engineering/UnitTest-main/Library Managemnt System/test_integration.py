import unittest
from library import Library
from book import Book
from member import Member

class TestLibraryIntegration(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.book = Book("B01", "1984")
        self.member = Member("M01", "Bob")

    def test_issue_flow_updates_both(self):
        self.library.issue_book(self.member, self.book)
        
        # Verify both units synchronized state correctly
        self.assertFalse(self.book.is_available)
        self.assertIn("1984", self.member.list_borrowed())

    def test_receive_flow_updates_both(self):
        # Setup initial borrowed state
        self.library.issue_book(self.member, self.book)
        
        # Test recovery
        self.library.receive_book(self.member, self.book)
        self.assertTrue(self.book.is_available)
        self.assertEqual(len(self.member.list_borrowed()), 0)

if __name__ == "__main__":
    unittest.main()