import streamlit as st
from entendimiento2 import Book, Library, Member, Librarian

# Function to initialize session state
def reset_session():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.current_user = None
    st.session_state.registering = False
    st.session_state.show_books = False
    st.session_state.show_members = False
    st.session_state.borrow_book_id = ""
    st.session_state.return_book_id = ""
    st.session_state.new_password = ""
    st.session_state.new_book_title = ""
    st.session_state.new_book_author = ""
    st.session_state.new_book_id = ""
    st.session_state.remove_book_id = ""
    st.session_state.change_password = False

# Initialize library and sample data
if 'library' not in st.session_state:
    st.session_state.library = Library()
    
    # Sample data
    books = [
        # Clasics
        Book("The Great Gatsby", "F. Scott Fitzgerald", 1),
        Book("1984", "George Orwell", 2),
        Book("Brave New World", "Aldous Huxley", 3),
        Book("To Kill a Mockingbird", "Harper Lee", 4),
        
        
        # Popular moderns
        Book("The Hunger Games", "Suzanne Collins", 5),
        Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 6),
        
        
        # Non-fiction
        Book("Sapiens", "Yuval Noah Harari", 7),
        Book("Atomic Habits", "James Clear", 8),
        
        
        # Additional various
        Book("The Lord of the Rings", "J.R.R. Tolkien", 9),
        Book("The Martian", "Andy Weir", 10)
    ]
    
    
    for book in books:
        st.session_state.library.add_book(book)
    
    member1 = Member("Alice", "secure123", 1001)
    member2 = Member("Bob", "password456", 1002)
    
    librarian1 = Librarian("Charlie", "admin123", 2001, st.session_state.library)
    
    st.session_state.library.add_member(member1)
    st.session_state.library.add_member(member2)
    
    st.session_state.library.add_librarian(librarian1)

# Initialize session state
if 'logged_in' not in st.session_state:
    reset_session()

# Main function
def main():
    st.title("📚 Library Management System")
    
    # Login/registration page
    if not st.session_state.logged_in:
        if not st.session_state.registering:
            show_login_page()
        else:
            show_registration_page()
    else:
        # Page for authenticated users
        if isinstance(st.session_state.current_user, Member):
            show_member_interface()
        elif isinstance(st.session_state.current_user, Librarian):
            show_librarian_interface()

# Show login page
def show_login_page():
    st.subheader("Login")
    st.session_state.user_type = st.radio("Select your role:", ("Member", "Librarian", "Register"))
    
    if st.session_state.user_type in ["Member", "Librarian"]:
        user_id = st.number_input(f"{st.session_state.user_type} ID", min_value=1, step=1)
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            authenticate_user(user_id, password)
    else:
        if st.button("Register"):
            st.session_state.registering = True
            st.rerun()

# Authenticate user
def authenticate_user(user_id, password):
    if st.session_state.user_type == "Member":
        members = st.session_state.library._Library__members
        if user_id in members and members[user_id].password == password:
            st.session_state.current_user = members[user_id]
            st.session_state.logged_in = True
            st.success("Logged in as member!")
        else:
            st.error("Invalid member ID or password")
    else:  # Librarian
        librarians = st.session_state.library._Library__librarians
        if user_id in librarians and librarians[user_id].password == password:
            st.session_state.current_user = librarians[user_id]
            st.session_state.logged_in = True
            st.success("Logged in as librarian!")
        else:
            st.error("Invalid librarian ID or password")
    st.rerun()

# Show registration page
def show_registration_page():
    st.subheader("Registration")
    new_user_type = st.radio("Register as:", ("Member", "Librarian"))
    new_name = st.text_input("Name")
    new_id = st.number_input("ID", min_value=1, step=1)
    new_password = st.text_input("Password", type="password")
    
    if st.button("Complete Registration"):
        register_user(new_user_type, new_name, new_id, new_password)
    
    if st.button("Back to Login"):
        st.session_state.registering = False
        st.rerun()

# Register new user
def register_user(user_type, name, user_id, password):
    if len(password) < 6:
        st.error("Password must be at least 6 characters")
        return
    
    # Verificar si el ID ya existe (tanto para miembros como bibliotecarios)
    all_members = st.session_state.library._Library__members
    all_librarians = st.session_state.library._Library__librarians
    
    if user_type == "Member":
        if user_id in all_members:
            st.error(f"Registration failed: The ID {user_id} is already in use by another member.")
            return  # Detener el registro aquí
        else:
            new_member = Member(name, password, user_id)
            st.session_state.library.add_member(new_member)
            st.success("Member registered successfully! Please login.")
    else:  # Librarian
        if user_id in all_librarians:
            st.error(f"Registration failed: The ID {user_id} is already in use by another librarian.")
            return
        else:
            new_librarian = Librarian(name, password, user_id, st.session_state.library)
            st.session_state.library.add_librarian(new_librarian)
            st.success("Librarian registered successfully! Please login.")
    
    st.session_state.registering = False
    st.rerun()

# Show member interface
def show_member_interface():
    st.subheader(f"👤 Member: {st.session_state.current_user.name}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Available Books"):
            st.session_state.show_books = not st.session_state.show_books
            if st.session_state.show_books:
                st.session_state.show_members = False
    
    with col2:
        if st.button("Change Password"):
            st.session_state.change_password = not st.session_state.change_password
    
    if st.session_state.show_books:
        show_books_for_member()
    
    if st.session_state.change_password:
        change_password_interface()
    
    if st.button("Logout"):
        reset_session()
        st.rerun()

# Show books for members
def show_books_for_member():
    books = st.session_state.library.show_books()
    if books:
        st.write("### Available Books:")
        for book_id, book_info in books.items():
            st.write(book_info)
        
        st.write("### Manage Loans")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.borrow_book_id = st.number_input("Book ID to borrow", min_value=1, step=1)
            if st.button("Borrow Book"):
                try:
                    book = st.session_state.library._Library__books.get(st.session_state.borrow_book_id)
                    if book:
                        if st.session_state.current_user.borrow_book(book):
                            st.success(f"Book '{book.title}' borrowed successfully!")
                            st.rerun()
                    else:
                        st.error("Book not found")
                except ValueError as e:
                    st.error(str(e))
        
        with col2:
            st.session_state.return_book_id = st.number_input("Book ID to return", min_value=1, step=1)
            if st.button("Return Book"):
                try:
                    book = st.session_state.library._Library__books.get(st.session_state.return_book_id)
                    if book:
                        if st.session_state.return_book_id in st.session_state.current_user._Member__borrowed_books:
                            st.session_state.current_user.return_book(book)
                            st.success(f"Book '{book.title}' returned successfully!")
                            st.rerun()
                        else:
                            st.error("You didn't borrow this book")
                    else:
                        st.error("Book not found")
                except ValueError as e:
                    st.error(str(e))
    else:
        st.write("No books available in the library.")

# Show librarian interface
def show_librarian_interface():
    st.subheader(f"👔 Librarian: {st.session_state.current_user.name}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View Books"):
            st.session_state.show_books = not st.session_state.show_books
            if st.session_state.show_books:
                st.session_state.show_members = False
    
    with col2:
        if st.button("View Members"):
            st.session_state.show_members = not st.session_state.show_members
            if st.session_state.show_members:
                st.session_state.show_books = False
    
    with col3:
        if st.button("Change Password"):
            st.session_state.change_password = not st.session_state.change_password
    
    if st.session_state.show_books:
        show_books_for_librarian()
    
    if st.session_state.show_members:
        show_members_list()
    
    if st.session_state.change_password:
        change_password_interface()
    
    if st.button("Logout"):
        reset_session()
        st.rerun()

# Show books for librarians
def show_books_for_librarian():
    st.write("### Book Management")
    books = st.session_state.library.show_books()
    if books:
        st.write("#### Current Books in Library:")
        for book_id, book_info in books.items():
            st.write(book_info)
    
    st.write("#### Add New Book")
    st.session_state.new_book_title = st.text_input("Book Title")
    st.session_state.new_book_author = st.text_input("Author")
    st.session_state.new_book_id = st.number_input("Book ID", min_value=1, step=1)
    
    if st.button("Add Book"):
        try:
            new_book = Book(
                st.session_state.new_book_title,
                st.session_state.new_book_author,
                st.session_state.new_book_id
            )
            st.session_state.current_user.add_book(new_book)
            st.success("Book added successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))
    
    st.write("#### Remove Book")
    st.session_state.remove_book_id = st.number_input("Book ID to remove", min_value=1, step=1)
    if st.button("Remove Book"):
        try:
            st.session_state.current_user.remove_book(st.session_state.remove_book_id)
            st.success("Book removed successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))

# Show members list
def show_members_list():
    st.write("### Members List")
    members = st.session_state.library.show_members()
    if members:
        for member_id, member_name in members.items():
            st.write(f"{member_name} (ID: {member_id})")
    else:
        st.write("No members registered.")

# Change password interface
def change_password_interface():
    st.write("### Change Password")
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Password"):
        if len(new_password) < 6:
            st.error("Password must be at least 6 characters")
        else:
            st.session_state.current_user.password = new_password
            st.success("Password updated successfully!")
            st.session_state.change_password = False
            st.rerun()

if __name__ == "__main__":
    main()
