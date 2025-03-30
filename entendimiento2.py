from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, book_id):
        self.__title = title
        self.__author = author
        self.__book_id = book_id
        self.__available = True  # Estado de disponibilidad
        
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
    

    def borrow(self):
        if self.__available:
            self.__available = False
            return True
        return False

    def return_book(self):
        if self.__available:  
            raise ValueError("Book is already returned.")
        else:
            self.__available = True  

    def __str__(self):
        return f"(ID: {self.__book_id}) {self.__title} by {self.author}  - {'Available' if self.__available else 'Not Available'}"

class Library:
    def __init__(self):
        self.__books = {}
        self.__members = {}
        self.__librarians = {}
        #self._transactions = []
    
    def add_book(self, book):
        if not isinstance(book, Book):
            raise ValueError("Invalid book.")
        if book.book_id in self.__books:
            print("This book is already in the library.")
        else:
            self.__books[book.book_id] = book
    
    def remove_book(self, book_id):
        if book_id in self.__books:
            del self.__books[book_id]
        else:
            print("Book not found in the library.")
    
    def show_books(self):
        return {book_id: str(book) for book_id, book in self.__books.items()}
    
    def show_members(self):
        return {member_id: member.name for member_id, member in self.__members.items()}
    
    def add_member(self, member):
        if isinstance(member, Member):
            if member.member_id in self.__members:
                print("This member is already registered.")
            else:
                self.__members[member.member_id] = member
                
    def remove_member(self, member_id):
        if member_id in self.__members:
            del self.__members[member_id]
        else:
            print("Member not found in the library.")
            
    def add_librarian(self, librarian):
        if isinstance(librarian, Librarian):
            if librarian.employee_id in self.__librarians:
                print("This librarian is already registered.")
            else:
                self.__librarians[librarian.employee_id] = librarian


class Member:
    BORROW_LIMIT = 3

    def __init__(self, name, password, member_id):
        self.__name = name
        self.__password = password
        self.__member_id = member_id
        self.__borrowed_books = {}
        
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
    def password(self, new_password):
        if len(new_password) < 6:
            print("Password must be at least 6 characters long.")
        else:
            self.__password = new_password
            

    def borrow_book(self, book):
        if len(self.__borrowed_books) >= self.BORROW_LIMIT:
            raise ValueError(f"{self.__name} has reached the borrowing limit!")
        
        if book.borrow():
            self.__borrowed_books[book.book_id] = book  # Añadir libro al diccionario
            print(f"{self.__name} borrowed '{book.title}'.")
            return True
        raise ValueError(f"{book.title} is not available.")

    def return_book(self, book):
        if book.book_id in self.__borrowed_books:
            book.return_book()
            del self.__borrowed_books[book.book_id]  # Eliminar libro del diccionario
            print(f"{self.__name} returned '{book.title}'.")
        else:
            print("This book was not borrowed by this member.")
            
    def __str__(self):
        return f"{self.__name} (ID: {self.__member_id})"

"""    def calculate_fine(self, due_date):
        overdue_days = (datetime.now() - due_date).days
        return max(0, overdue_days * 1.5)"""
    

    
    




class Librarian:
    def __init__(self, name, password, employee_id, library):
        self.__name = name
        self.__password = password
        self.__employee_id = employee_id
        self.__library = library

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

    def add_book(self, book):
        self.__library.add_book(book)
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, book_id):
        self.__library.remove_book(book_id)
        print(f"Book with ID {book_id} removed from the library.")

    def view_books(self):
        books = self.__library.show_books()
        if books:
            print("\nLibrary Books:")
            for book_id, book_info in books.items():
                print(f"{book_info} (ID: {book_id})")
        else:
            print("No books in the library.")

    def view_members(self):
        members = self.__library.show_members()
        print("\nRegistered Members:")
        for member_id, member_name in members.items():
            print(f"{member_name} (ID: {member_id})")
            
    def __str__(self):
        return f"{self.__name} (ID: {self.__employee_id})"
            
            
            



# Crear instancias de la biblioteca
library = Library()

# Crear libros
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1)
book2 = Book("1984", "George Orwell", 2)
book3 = Book("Brave New World", "Aldous Huxley", 3)

# Crear miembros
member1 = Member("Alice", "secure123", 1001)
member2 = Member("Bob", "password456", 1002)

# Crear bibliotecario
librarian1 = Librarian("Charlie", "admin123", 2001, library)

# Agregar libros a la biblioteca
library.add_book(book1)
library.add_book(book2)

# Agregar miembros a la biblioteca
library.add_member(member1)
library.add_member(member2)

# Agregar bibliotecario a la biblioteca
library.add_librarian(librarian1)

# Bibliotecario agrega un libro
librarian1.add_book(book3)

# mostrar libros

print ("Libros en la biblioteca")
print (library.show_books())

print ("Libros en la biblioteca por el bibliotecario")
print (librarian1.view_books())

print ("Miembros en la biblioteca")
print (library.show_members())

print ("Miembros en la biblioteca por el bibliotecario")
print (librarian1.view_members())

# Miembro toma prestado un libro
member1.borrow_book(book1)


print ("Libros en la biblioteca despues de que un miembro toma prestado un libro")
print (library.show_books())

# Miembro devuelve un libro
member1.return_book(book1)






"""# Agregar libros a la biblioteca
add_book1 = library.add_book(book1)
add_book2 = library.add_book(book2)

# Crear miembro
member1 = Member("Alice", "secure123", 1001)
library.add_member(member1)

# Miembro toma prestado un libro
borrow_result = member1.borrow_book(book1)

# Mostrar estado de los libros
books_after_borrow = library.show_books()

# Miembro devuelve el libro
return_result = member1.return_book(book1)

# Mostrar estado final de los libros
books_after_return = library.show_books()

(add_book1, add_book2, borrow_result, books_after_borrow, return_result, books_after_return)"""
            


