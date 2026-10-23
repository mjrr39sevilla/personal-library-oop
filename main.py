from book import Book

book = Book("Africanus", "Santiago Posteguillo")
print(book)

book.mark_as_read()
print(book)

book.copies = 2
print(book.is_duplicated())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
