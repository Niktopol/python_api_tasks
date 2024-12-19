from strawberry import type, field
from typing import List, Optional
from strawberry import Info
from models import Book, Library, Author

@type
class LibraryType:
    id: int
    name: str
    @field
    def books(self, info) -> List['BookType']:
        db = info.context['db']
        books = db.query(Book).filter(Book.library_id == self.id).all()
        return [BookType(id=book.id, title=book.title) for book in books]

@type
class AuthorType:
    id: int
    name: str
    @field
    def books(self, info) -> List['BookType']:
        db = info.context['db']
        books = db.query(Book).filter(Book.author_id == self.id).all()
        return [BookType(id=book.id, title=book.title) for book in books]

@type
class BookType:
    id: int
    title: str
    @field
    def author(self, info) -> AuthorType:
        db = info.context['db']
        author = db.query(Author).filter(Author.id == db.query(Book).filter(Book.id == self.id).first().author_id).first()
        return AuthorType(id=author.id, name=author.name)
    @field
    def library(self, info) -> LibraryType:
        db = info.context['db']
        library = db.query(Library).filter(Library.id == db.query(Book).filter(Book.id == self.id).first().library_id).first()
        return LibraryType(id=library.id, name=library.name)

def get_all_books(info: Info):
    db = info.context['db']
    books = db.query(Book).all()
    return [BookType(id=book.id, title=book.title) for book in books]

def get_book_by_id(book_id: int, info: Info):
    db = info.context['db']
    book = db.query(Book).filter(Book.id==book_id).first()
    if book:
        return BookType(id=book.id, title=book.title)
    return None

def get_books_by_author(author_id: int, info: Info):
    db = info.context['db']
    books = db.query(Book).filter(Book.author_id==author_id).all()
    return [BookType(id=book.id, title=book.title) for book in books]

def get_books_by_library(library_id: int, info: Info):
    db = info.context['db']
    books = db.query(Book).filter(Book.library_id==library_id).all()
    return [BookType(id=book.id, title=book.title) for book in books]

def get_all_authors(info: Info):
    db = info.context['db']
    authors = db.query(Author).all()
    return [AuthorType(id=author.id, name=author.name) for author in authors]

def get_author_by_id(author_id: int, info: Info):
    db = info.context['db']
    author = db.query(Author).filter(Author.id==author_id).first()
    if author:
        return AuthorType(id=author.id, nane=author.name)
    return None

def get_all_libraries(info: Info):
    db = info.context['db']
    libraries = db.query(Library).all()
    return [LibraryType(id=library.id, name=library.name) for library in libraries]

def get_library_by_id(library_id: int, info: Info):
    db = info.context['db']
    library = db.query(Library).filter(Author.id==library_id).first()
    if library:
        return Library(id=library.id, nane=library.name)
    return None

def add_book(title: str, author_id: int, library_id: int, info: Info):
    try:
        db = info.context['db']
        _book = Book(title=title, author_id=author_id, library_id=library_id)
        db.add(_book)
        db.commit()
        db.refresh(_book)
        return _book
    except:
        return None

def add_author(name: str, info: Info):
    try:
        db = info.context['db']
        _author = Author(name=name)
        db.add(_author)
        db.commit()
        db.refresh(_author)
        return _author
    except:
        return None

def add_library(name: str, info: Info):
    try:
        db = info.context['db']
        _library = Library(name=name)
        db.add(_library)
        db.commit()
        db.refresh(_library)
        return _library
    except:
        return None

def delete_book(book_id: int, info: Info):
    try:
        db = info.context['db']
        _book = db.query(Book).filter(Book.id == book_id).first()
        db.delete(_book)
        db.commit()
        return True
    except:
        return False

def delete_author(author_id: int, info: Info):
    try:
        db = info.context['db']
        _author = db.query(Author).filter(Author.id == author_id).first()
        db.delete(_author)
        db.commit()
        return True
    except:
        return False 

def delete_library(library_id: int, info: Info):
    try:
        db = info.context['db']
        _library = db.query(Library).filter(Library.id == library_id).first()
        db.delete(_library)
        db.commit()
        return True
    except:
        return False

@type
class Query:
    get_all_books: List[BookType] = field(resolver=get_all_books)
    get_book_by_id: Optional[BookType] = field(resolver=get_book_by_id)
    get_books_by_author: List[BookType] = field(resolver=get_books_by_author)
    get_books_by_library: List[BookType] = field(resolver=get_books_by_library)
    get_all_authors: List[AuthorType] = field(resolver=get_all_authors)
    get_author_by_id: Optional[AuthorType] = field(resolver=get_author_by_id)
    get_all_libraries: List[LibraryType] = field(resolver=get_all_libraries)
    get_library_by_id: Optional[LibraryType] = field(resolver=get_library_by_id)

@type
class Mutation:
    add_book: Optional[BookType] = field(resolver=add_book)
    add_author: Optional[AuthorType] = field(resolver=add_author)
    add_library: Optional[LibraryType] = field(resolver=add_library)
    delete_book: bool = field(resolver=delete_book)
    delete_author: bool = field(resolver=delete_author)
    delete_library: bool = field(resolver=delete_library)