class Library:

    def issue_book(self, member, book):
        if book.borrow_book():
            member.add_book(book.title)
            return f"Issued {book.title} to {member.name}"

    def receive_book(self, member, book):
        if book.return_book():
            member.remove_book(book.title)
            return f"Returned {book.title} from {member.name}"