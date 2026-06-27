class Member:

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def add_book(self, book_title):
        self.borrowed_books.append(book_title)

    def remove_book(self, book_title):
        if book_title not in self.borrowed_books:
            raise ValueError("Member does not have this book")
        self.borrowed_books.remove(book_title)

    def list_borrowed(self):
        return self.borrowed_books