from book import Book
from library import Library


def show_books(books):
    if not books:
        print("No hay libros para mostrar.")
        return
    for book in books:
        print(book)


def add_book_option(library):
    title = input("Título del libro: ").strip()
    author = input("Autor: ").strip()
    if not title or not author:
        print("El título y el autor no pueden estar vacíos.")
        return
    has_read = input("¿Ya lo has leído? (s/n): ").strip().lower()
    status = "read" if has_read == "s" else "to_read"
    is_new = library.add_book(Book(title, author, status))
    if is_new:
        print("Libro añadido a la biblioteca.")
    else:
        print("Ese libro ya existía: se ha sumado un ejemplar (duplicado).")


def mark_as_read_option(library):
    title = input("Título del libro que has leído: ").strip()
    if library.mark_as_read(title):
        print("Libro marcado como leído.")
    else:
        print("No se ha encontrado ese libro.")


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
        elif option == "0":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Prueba otra vez.")


if __name__ == "__main__":
    main()