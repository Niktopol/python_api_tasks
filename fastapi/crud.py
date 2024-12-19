from sqlalchemy.orm import Session, joinedload
from models import *
from schemas import *

def get_books(db: Session):
    return db.query(Book).all()

def create_book(db: Session, book: BookСreate):
    _book = Book(**book.model_dump())
    db.add(_book)
    db.commit()
    db.refresh(_book)

def put_book(db: Session, book: BookPut):
    _book = db.query(Book).filter(Book.id == book.id).first()
    _book.title = book.title
    _book.author_id = book.author_id
    _book.library_id = book.library_id
    db.commit()
    db.refresh(_book)

def patch_book(db: Session, book: BookPatch):
    _book = db.query(Book).filter(Book.id == book.id).first()
    if book.title:
        _book.title = book.title
    if book.author_id:
        _book.author_id = book.author_id
    if book.library_id:
        _book.library_id = book.library_id
    db.commit()
    db.refresh(_book)

def delete_book(db: Session, id: int):
    _book = db.query(Book).filter(Book.id == id).first()
    db.delete(_book)
    db.commit()

def get_authors(db: Session):
    return db.query(Author).all()

def create_author(db: Session, author: AuthLibBase):
    _author = Author(**author.model_dump())
    db.add(_author)
    db.commit()
    db.refresh(_author)

def put_author(db: Session, author: AuthLibPut):
    _author = db.query(Author).filter(Author.id == author.id).first()
    _author.name = author.name
    db.commit()
    db.refresh(_author)

def patch_author(db: Session, author: AuthLibPatch):
    _author = db.query(Author).filter(Author.id == author.id).first()
    if author.name:
        _author.name = author.name
    db.commit()
    db.refresh(_author)

def delete_author(db: Session, id: int):
    _author = db.query(Author).filter(Author.id == id).first()
    db.delete(_author)
    db.commit()

def get_libraries(db: Session):
    return db.query(Library).all()

def create_library(db: Session, library: AuthLibBase):
    _library = Library(**library.model_dump())
    db.add(_library)
    db.commit()
    db.refresh(_library)

def put_library(db: Session, library: AuthLibPut):
    _library = db.query(Library).filter(Library.id == library.id).first()
    _library.name = library.name
    db.commit()
    db.refresh(_library)

def patch_library(db: Session, library: AuthLibPatch):
    _library = db.query(Library).filter(Library.id == library.id).first()
    if library.name:
        _library.name = library.name
    db.commit()
    db.refresh(_library)

def delete_library(db: Session, id: int):
    _library = db.query(Library).filter(Library.id == id).first()
    db.delete(_library)
    db.commit()