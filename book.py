from abc import ABC, abstractmethod
from datetime import date


class Book(ABC):
    """Abstract parent class: it cannot be created directly."""

    def __init__(self, title, author, copies=1):
        self.title = title
        self.author = author
        self.copies = copies

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        value = value.strip()
        if not value:
            raise ValueError("El título no puede estar vacío.")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        value = value.strip()
        if not value:
            raise ValueError("El autor no puede estar vacío.")
        self._author = value

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        if value < 1:
            raise ValueError("Un libro debe tener al menos un ejemplar.")
        self._copies = value

    @property
    @abstractmethod
    def status(self):
        """Reading status: 'read' or 'to_read'."""

    @abstractmethod
    def reading_info(self):
        """Short text about the reading state, shown when printing the book."""

    @abstractmethod
    def mark_as_read(self, date_read=None):
        """Return the book as a ReadBook."""

    def is_duplicated(self):
        return self.copies > 1

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "copies": self.copies,
        }

    @staticmethod
    def from_dict(data):
        if data["status"] == "read":
            date_read = data.get("date_read")
            if date_read:
                date_read = date.fromisoformat(date_read)
            return ReadBook(data["title"], data["author"], data["copies"], date_read or None)
        return PendingBook(data["title"], data["author"], data["copies"])

    def __str__(self):
        return f"{self.title} - {self.author} [{self.status}] x{self.copies} ({self.reading_info()})"


class PendingBook(Book):
    """A book that has not been read yet: it has no reading date."""

    @property
    def status(self):
        return "to_read"

    def reading_info(self):
        return "pendiente de leer"

    def mark_as_read(self, date_read=None):
        return ReadBook(self.title, self.author, self.copies, date_read or date.today())

    def to_dict(self):
        data = super().to_dict()
        data["date_read"] = None
        return data


class ReadBook(Book):
    """A book that has already been read: it keeps its reading date."""

    def __init__(self, title, author, copies=1, date_read=None):
        super().__init__(title, author, copies)
        self._date_read = date_read

    @property
    def status(self):
        return "read"

    @property
    def date_read(self):
        return self._date_read

    def reading_info(self):
        date_text = self._date_read.isoformat() if self._date_read else "—"
        return f"leído: {date_text}"

    def mark_as_read(self, date_read=None):
        return self

    def to_dict(self):
        data = super().to_dict()
        data["date_read"] = self._date_read.isoformat() if self._date_read else None
        return data