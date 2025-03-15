import streamlit as st
import json
import os

data_file = "library.txt"

# Load library data
def load_library():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

# Save library data
def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file, indent=4)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Streamlit UI
st.title("📚 Library Management System")

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "List Books", "Display All Books", "Display Stats"])

# Add a book
if menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Enter title:")
    author = st.text_input("Enter author:")
    year = st.text_input("Enter year:")
    genre = st.text_input("Enter genre:")
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        st.session_state.library.append(new_book)
        save_library(st.session_state.library)
        st.success(f"Book '{title}' by {author} added to the library!")

# Remove a book
elif menu == "Remove Book":
    st.header("Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    book_to_remove = st.selectbox("Select book to remove", ["Select"] + titles)
    
    if st.button("Remove Book") and book_to_remove != "Select":
        st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
        save_library(st.session_state.library)
        st.success(f"Book '{book_to_remove}' removed from the library!")

# List books based on criteria
elif menu == "List Books":
    st.header("List Books")
    search_by = st.selectbox("Search by", ["title", "author", "year", "genre", "read"])
    search_term = st.text_input(f"Enter the {search_by}:")
    
    if st.button("Search"):
        results = [book for book in st.session_state.library if search_term.lower() in str(book[search_by]).lower()]
        if results:
            for book in results:
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No books found!")

# Display all books
elif menu == "Display All Books":
    st.header("All Books in Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.warning("No books in the library!")

# Display library statistics
elif menu == "Display Stats":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    total_read = sum(book["read"] for book in st.session_state.library)
    total_unread = total_books - total_read
    percentage_read = (total_read / total_books) * 100 if total_books else 0
    
    st.write(f"Total books: {total_books}")
    st.write(f"Total read: {total_read}")
    st.write(f"Total unread: {total_unread}")
    st.write(f"Percentage read: {percentage_read:.2f}%")
