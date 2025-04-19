class Book:
    def __init__(self, title, author, book_id):
        self.__title = title        # Private attribute for book title
        self.__author = author      # Private attribute for author name
        self.__book_id = book_id    # Private attribute for unique book ID
        self.__available = True     # Private attribute to track availability
        
    @property
    def title(self):
        return self.__title
    
    @property
    def author(self):
        return self.__author
    
    @property
    def book_id(self):
        return self.__book_id
    
    @property
    def availability(self):
        return self.__available
    

    def borrow(self):                # Marks the book as unavailable if it’s currently available.
        if self.__available:
            self.__available = False
            return True
        return False

    def return_book(self):            # Marks the book as available and raises an error if already returned.
        if self.__available:  
            raise ValueError("Book is already returned.")
        else:
            self.__available = True  

    def __str__(self):                # Provides a user-friendly string representation of the book.
        return f"(ID: {self.__book_id}) {self.__title} by {self.author}  - {'Available' if self.__available else 'Not Available'}"

class Library:
    def __init__(self):
        self.__books = {}             # Dictionary to store books (key: book_id)
        self.__members = {}           # Dictionary to store members (key: member_id)
        self.__librarians = {}        # Dictionary to store librarians (key: employee_id)
    
    def add_book(self, book):         # Validates and manages book additions.
        if not isinstance(book, Book):
            raise ValueError("Invalid book.")
        if book.book_id in self.__books:
            print("This book is already in the library.")
        else:
            self.__books[book.book_id] = book
    
    def remove_book(self, book_id):   # Validates and manages book removals.
        if book_id in self.__books:
            del self.__books[book_id]
        else:
            print("Book not found in the library.")
    
    def show_books(self):             # Returns formatted lists of books.
        return {book_id: str(book) for book_id, book in self.__books.items()}
    
    def show_members(self):           # Returns formatted lists of members.
        return {member_id: member.name for member_id, member in self.__members.items()}
    
    def add_member(self, member):     # Handles member registration.
        if isinstance(member, Member):
            if member.member_id in self.__members:
                print("This member is already registered.")
            else:
                self.__members[member.member_id] = member
                
    def remove_member(self, member_id): # Handles member registration/deregistration.
        if member_id in self.__members:
            del self.__members[member_id]
        else:
            print("Member not found in the library.")
            
    def add_librarian(self, librarian):    # # Handles librarian registration
        if isinstance(librarian, Librarian):
            if librarian.employee_id in self.__librarians:
                print("This librarian is already registered.")
            else:
                self.__librarians[librarian.employee_id] = librarian


class Member:
    BORROW_LIMIT = 3     # Class-level constant for max books a member can borrow

    def __init__(self, name, password, member_id):
        self.__name = name            # Member's name.
        self.__password = password    # Password (validated via setter).
        self.__member_id = member_id    # Unique Member ID.
        self.__borrowed_books = {}    # Dictionary to track borrowed books {book_id: Book}.
        
    @property
    def name(self):
        return self.__name
    
    @property
    def password(self):
        return self.__password
    
    @property
    def member_id(self):
        return self.__member_id
    
    @property
    def borrowed_books(self):
        return self.__borrowed_books
    
    @password.setter
    def password(self, new_password):     # The password setter enforces a minimum length of 6 characters.
        if len(new_password) < 6:
            print("Password must be at least 6 characters long.")
        else:
            self.__password = new_password
            

    def borrow_book(self, book):        # Checks if the member hasn’t exceeded BORROW_LIMIT and updates
        if len(self.__borrowed_books) >= self.BORROW_LIMIT:
            raise ValueError(f"{self.__name} has reached the borrowing limit!")
        
        if book.borrow():
            self.__borrowed_books[book.book_id] = book  
            print(f"{self.__name} borrowed '{book.title}'.")
            return True
        raise ValueError(f"{book.title} is not available.")

    def return_book(self, book):        # Validates returns and updates availability
        if book.book_id in self.__borrowed_books:
            book.return_book()
            del self.__borrowed_books[book.book_id]  
            print(f"{self.__name} returned '{book.title}'.")
        else:
            print("This book was not borrowed by this member.")
            
    def __str__(self):
        return f"{self.__name} (ID: {self.__member_id})"


class Librarian:
    def __init__(self, name, password, employee_id, library):
        self.__name = name        # Librarian's name.
        self.__password = password        # Password (validated via setter).
        self.__employee_id = employee_id        # Unique employee ID.
        self.__library = library        # Reference to the Library instance for delegation.

    @property
    def name(self):
        return self.__name

    @property
    def password(self):
        return self.__password

    @property
    def employee_id(self):
        return self.__employee_id

    @password.setter
    def password(self, new_password):
        if len(new_password) < 6:
            print("Password must be at least 6 characters long.")
        else:
            self.__password = new_password

    def add_book(self, book):    # Delegates to Library.add_book() and prints confirmation.
        self.__library.add_book(book)
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, book_id):    # Delegates to Library.remove_book() and prints confirmation.
        self.__library.remove_book(book_id)
        print(f"Book with ID {book_id} removed from the library.")

    def view_books(self):        # Displays all books in the library via Library.show_books().
        books = self.__library.show_books()
        if books:
            print("\nLibrary Books:")
            for book_id, book_info in books.items():
                print(f"{book_info} (ID: {book_id})")
        else:
            print("No books in the library.")

    def view_members(self):        # Displays all members via Library.show_members().
        members = self.__library.show_members()
        print("\nRegistered Members:")
        for member_id, member_name in members.items():
            print(f"{member_name} (ID: {member_id})")
            
    def __str__(self): # String representation (e.g., 'Charlie (ID: 2001)').
        return f"{self.__name} (ID: {self.__employee_id})"
            
            
            



# Create library instances
library = Library()

# Create books
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1)
book2 = Book("1984", "George Orwell", 2)
book3 = Book("Brave New World", "Aldous Huxley", 3)

# Create members
member1 = Member("Alice", "secure123", 1001)
member2 = Member("Bob", "password456", 1002)

# Create librarian
librarian1 = Librarian("Charlie", "admin123", 2001, library)

# Add books to the library
library.add_book(book1)
library.add_book(book2)

# Add members to the library
library.add_member(member1)
library.add_member(member2)

# Add librarian to the library
library.add_librarian(librarian1)

# Librarian adds a book
librarian1.add_book(book3)

# show books

print ("Libros en la biblioteca")
print (library.show_books())

print ("Libros en la biblioteca por el bibliotecario")
print (librarian1.view_books())

print ("Miembros en la biblioteca")
print (library.show_members())

print ("Miembros en la biblioteca por el bibliotecario")
print (librarian1.view_members())

# Member borrows a book
member1.borrow_book(book1)


print ("Libros en la biblioteca despues de que un miembro toma prestado un libro")
print (library.show_books())

# Member returns a book
member1.return_book(book1)

