import json
import shutil
from pathlib import Path

from book import Book

DEFAULT_FILE = Path(__file__).parent / "books.json"


class Library:
    def __init__(self, file_path=DEFAULT_FILE):
        self.books = []
        self.file_path = Path(file_path)
        self.load()

    def save(self):
        data = [book.to_dict() for book in self.books]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            backup_path = Path(str(self.file_path) + ".bak")
            shutil.copy(self.file_path, backup_path)
            print(f"El archivo de libros está dañado. Copia guardada en {backup_path.name}.")
            return
        self.books = [Book.from_dict(item) for item in data]

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def add_book(self, book):
        existing_book = self.find_book(book.title)
        if existing_book:
            existing_book.copies += 1
            self.save()
            return False
        self.books.append(book)
        self.save()
        return True

    def mark_as_read(self, title, date_read=None):
        book = self.find_book(title)
        if book is None:
            return False
        book.mark_as_read(date_read)
        self.save()
        return True

    def edit_title(self, old_title, new_title):
        book = self.find_book(old_title)
        if book is None:
            return "not_found"
        other_book = self.find_book(new_title)
        if other_book is not None and other_book is not book:
            return "already_exists"
        book.title = new_title
        self.save()
        return "updated"

    def remove_book(self, title, remove_all=True):
        book = self.find_book(title)
        if book is None:
            return "not_found"
        if not remove_all and book.copies > 1:
            book.copies -= 1
            self.save()
            return "copy_removed"
        self.books.remove(book)
        self.save()
        return "removed"

    def get_books_by_status(self, status):
        return [book for book in self.books if book.status == status]

    def get_duplicated_books(self):
        return [book for book in self.books if book.is_duplicated()]