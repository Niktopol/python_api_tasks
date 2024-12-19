from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Book(Base):
    __tablename__ ="books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    library_id = Column(Integer, ForeignKey("libraries.id"))

    author = relationship("Author", back_populates="books")
    library = relationship("Library", back_populates="books")

class Author(Base):
    __tablename__ ="authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Library(Base):
    __tablename__ ="libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    books = relationship("Book", back_populates="library", cascade="all, delete-orphan")