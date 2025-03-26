import json
import os

data_file = "library.txt"


#  --------functions

# load data from file
def load_library():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


# save data to file
def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file, indent=4)


# add book
def add_book(library):
    title = input("Enter title: ")
    author = input("Enter author: ")
    year = input("Enter year: ")
    genre = input("Enter genre: ")
    read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }

    library.append(new_book)
    save_library(library)
    print(f"Book '{title}' by {author} added to the library!")


# remove books
def remove_book(library):
    title = input("Enter title of the book to remove: ").strip().lower()
    new_library = [book for book in library if book["title"].strip().lower() != title]

    if len(new_library) == len(library):
        print(f"Book '{title}' not found in the library!")
    else:
        save_library(new_library)
        print(f"Book '{title}' removed from the library!")
        return new_library  # Return updated library
    return library


# list books
def list_books(library):
    search_by = input("Search by title, author, year, genre, or read: ").strip().lower()

    if search_by not in ["title", "author", "year", "genre", "read"]:
        print("Invalid search criteria!")
        return

    search_term = input(f"Enter the {search_by}: ").strip().lower()

    results = [book for book in library if search_term in str(book[search_by]).strip().lower()]

    if results:
        for book in results:
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'read' if book['read'] else 'unread'}")
    else:
        print("No books found!")


# display all books
def display_books(library):
    if library:
        for book in library:
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'read' if book['read'] else 'unread'}")
    else:
        print("No books in the library!")


# display stats
def display_stats(library):
    total_books = len(library)
    total_read = sum(book["read"] for book in library)
    total_unread = total_books - total_read
    percentage_read = (total_read / total_books) * 100 if total_books else 0

    print(f"Total books: {total_books}")
    print(f"Total read: {total_read}")
    print(f"Total unread: {total_unread}")
    print(f"Percentage read: {percentage_read:.2f}%")


#  --------main
def main():
    library = load_library()

    while True:
        print("\nWelcome to the Library!")
        print("1. Add book")
        print("2. Remove book")
        print("3. List books")
        print("4. Display all books")
        print("5. Display stats")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_book(library)
        elif choice == "2":
            library = remove_book(library)  # Update library after removing a book
        elif choice == "3":
            list_books(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_stats(library)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
