from datetime import date


class Book:
    def __init__(self, title, author, status="to_read", copies=1, date_read=None):
        self.title = title
        self.author = author
        self.status = status
        self.copies = copies
        self.date_read = date_read

    def mark_as_read(self, date_read=None):
        self.status = "read"
        self.date_read = date_read if date_read is not None else date.today()

    def is_duplicated(self):
        return self.copies > 1

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "copies": self.copies,
            "date_read": self.date_read.isoformat() if self.date_read else None,
        }

    @classmethod
    def from_dict(cls, data):
        date_read = data.get("date_read")
        if date_read:
            date_read = date.fromisoformat(date_read)
        return cls(data["title"], data["author"], data["status"], data["copies"], date_read)

    def __str__(self):
        fecha = self.date_read.isoformat() if self.date_read else "—"
        return f"{self.title} - {self.author} [{self.status}] x{self.copies} (leído: {fecha})"
