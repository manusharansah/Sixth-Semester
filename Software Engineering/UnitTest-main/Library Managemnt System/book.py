class Book:

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.is_available = True

    def borrow_book(self):
        if not self.is_available:
            raise ValueError("Book is already borrowed")
        self.is_available = False
        return True

    def return_book(self):
        if self.is_available:
            raise ValueError("Book was not borrowed")
        self.is_available = True
        return True