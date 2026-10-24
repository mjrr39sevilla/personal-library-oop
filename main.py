import unicodedata

from datetime import date

from book import PendingBook, ReadBook
from library import Library

UNKNOWN_DATE = date(2022, 1, 1)
PAGE_SIZE = 20

def ask_date(message, default):
    text = input(f"{message} (AAAA-MM-DD, Enter = {default.isoformat()}): ").strip()
    if not text:
        return default
    try:
        return date.fromisoformat(text)
    except ValueError:
        print(f"Fecha no válida: se usa {default.isoformat()}.")
        return default


def title_sort_key(book):
    normalized = unicodedata.normalize("NFD", book.title.lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def show_books(books):
    if not books:
        print("No hay libros para mostrar.")
        return
    sorted_books = sorted(books, key=title_sort_key)
    total = len(sorted_books)
    for index, book in enumerate(sorted_books, start=1):
        print(f"{index}. {book}")
        if index % PAGE_SIZE == 0 and index < total:
            answer = input(f"--- {index} de {total} --- Enter para seguir, q para salir: ").strip().lower()
            if answer == "q":
                return
    print(f"--- Total: {total} libros ---")


def add_book_option(library):
    title = input("Título del libro: ").strip()
    author = input("Autor: ").strip()
    if not title or not author:
        print("El título y el autor no pueden estar vacíos.")
        return
    has_read = input("¿Ya lo has leído? (s/n): ").strip().lower()
    if has_read == "s":
        date_read = ask_date("Fecha de lectura", UNKNOWN_DATE)
        new_book = ReadBook(title, author, date_read=date_read)
    else:
        new_book = PendingBook(title, author)
    is_new = library.add_book(new_book)

    if is_new:
        print("Libro añadido a la biblioteca.")
    else:
        print("Ese libro ya existía: se ha sumado un ejemplar (duplicado).")


def mark_as_read_option(library):
    title = input("Título del libro que has leído: ").strip()
    book = library.find_book(title)
    if book is None:
        print("No se ha encontrado ese libro.")
        return
    if book.status == "read":
        print("Ese libro ya está marcado como leído.")
        return
    date_read = ask_date("Fecha de lectura", date.today())
    library.mark_as_read(title, date_read)
    print("Libro marcado como leído.")


def edit_title_option(library):
    old_title = input("Título actual del libro: ").strip()
    new_title = input("Nuevo título: ").strip()
    if not new_title:
        print("El nuevo título no puede estar vacío.")
        return
    result = library.edit_title(old_title, new_title)
    if result == "updated":
        print("Título modificado correctamente.")
    elif result == "already_exists":
        print("Ya existe otro libro con ese título.")
    else:
        print("No se ha encontrado ese libro.")


def remove_book_option(library):
    title = input("Título del libro que quieres dar de baja: ").strip()
    book = library.find_book(title)
    if book is None:
        print("No se ha encontrado ese libro.")
        return

    remove_all = True
    if book.copies > 1:
        answer = input(
            f"Tiene {book.copies} ejemplares. ¿Quitar solo uno (u) o todos (t)?: "
        ).strip().lower()
        if answer == "u":
            remove_all = False
        elif answer != "t":
            print("Opción no válida. Operación cancelada.")
            return

    confirm = input(f"¿Seguro que quieres dar de baja '{book.title}'? (s/n): ").strip().lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    result = library.remove_book(title, remove_all)
    if result == "copy_removed":
        print("Se ha quitado un ejemplar.")
    else:
        print("Libro dado de baja.")

def show_summary_option(library):
    summary = library.get_summary()
    print("\n--- Resumen de mi biblioteca ---")
    print(f"Libros distintos: {summary['titles']}")
    print(f"Ejemplares en total: {summary['copies']}")
    print(f"Leídos: {summary['read']}")
    print(f"Pendientes de leer: {summary['to_read']}")
    print(f"Con ejemplares duplicados: {summary['duplicated']}")

    by_year = library.get_read_by_year()
    if by_year:
        print("\nLeídos por año:")
        for year in sorted(by_year, reverse=True):
            print(f"  {year}: {by_year[year]}")

def list_by_author_option(library):
    author = input("Autor (basta con una parte del nombre): ").strip()
    if not author:
        print("El autor no puede estar vacío.")
        return
    show_books(library.get_books_by_author(author))

def main():
    library = Library()
    while True:
        print("\n--- Mi biblioteca personal ---")
        print("1. Añadir libro")
        print("2. Ver todos los libros")
        print("3. Ver libros leídos")
        print("4. Ver libros pendientes de leer")
        print("5. Ver libros duplicados")
        print("6. Marcar un libro como leído")
        print("7. Modificar el título de un libro")
        print("8. Dar de baja un libro")
        print("9. Ver resumen de mi biblioteca")
        print("10. Ver libros de un autor")
        print("0. Salir")
        option = input("Elige una opción: ").strip()

        if option == "1":
            add_book_option(library)
        elif option == "2":
            show_books(library.books)
        elif option == "3":
            show_books(library.get_books_by_status("read"))
        elif option == "4":
            show_books(library.get_books_by_status("to_read"))
        elif option == "5":
            show_books(library.get_duplicated_books())
        elif option == "6":
            mark_as_read_option(library)
        elif option == "7":
            edit_title_option(library)
        elif option == "8":
            remove_book_option(library)
        elif option == "9":
            show_summary_option(library)
        elif option == "10":
            list_by_author_option(library)
        elif option == "0":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Prueba otra vez.")


if __name__ == "__main__":
    main()