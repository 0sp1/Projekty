class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Checked out"
        return f"[{self.book_id}] {self.title} by {self.author} - {status}"


class Library:
    def __init__(self):
        self.books = []
        self.next_id = 1

    def add_book(self, title, author):
        book = Book(self.next_id, title, author)
        self.books.append(book)
        self.next_id += 1
        print(f"Book added: {book}")

    def view_books(self):
        if not self.books:
            print("No books in the library.")
            return
        print("\nLibrary Catalog:")
        for book in self.books:
            print(book)

    def checkout_book(self, book_id):
        book = self.find_book(book_id)
        if book and book.is_available:
            book.is_available = False
            print(f"You checked out: {book.title}")
        elif book:
            print("That book is already checked out.")
        else:
            print("Book not found.")

    def return_book(self, book_id):
        book = self.find_book(book_id)
        if book and not book.is_available:
            book.is_available = True
            print(f"Book returned: {book.title}")
        elif book:
            print("This book was not checked out.")
        else:
            print("Book not found.")

    def search_books(self, query):
        found_books = [
            book for book in self.books
            if query.lower() in book.title.lower() or query.lower() in book.author.lower()
        ]
        if found_books:
            print("\nSearch Results:")
            for book in found_books:
                print(book)
        else:
            print("No books found matching your search.")

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None


def main():
    library = Library()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add a book")
        print("2. View all books")
        print("3. Checkout a book")
        print("4. Return a book")
        print("5. Exit")
        print("6. Search for a book")  # New option

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)

        elif choice == "2":
            library.view_books()

        elif choice == "3":
            try:
                book_id = int(input("Enter book ID to checkout: "))
                library.checkout_book(book_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "4":
            try:
                book_id = int(input("Enter book ID to return: "))
                library.return_book(book_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "5":
            print("Exiting Library System. Goodbye!")
            break

        elif choice == "6":
            query = input("Enter title or author to search: ")
            library.search_books(query)

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
