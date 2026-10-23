class Library:
    def __init__(self):
        self.books = []

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def add_book(self, book):
        existing_book = self.find_book(book.title)
        if existing_book:
            existing_book.copies += 1
        else:
            self.books.append(book)