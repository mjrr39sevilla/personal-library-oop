class Book:
    def __init__(self, title, author, status="to_read", copies=1):
        self.title = title
        self.author = author
        self.status = status
        self.copies = copies

    def mark_as_read(self):
        self.status = "read"

    def is_duplicated(self):
        return self.copies > 1

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "copies": self.copies,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["status"], data["copies"])

    def __str__(self):
        return f"{self.title} - {self.author} [{self.status}] x{self.copies}"