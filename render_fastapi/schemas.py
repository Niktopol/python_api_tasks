from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from models import *

T = TypeVar('T')

class AuthLibBase(BaseModel):
    name: str

class AuthLibGet(AuthLibBase):
    id: int
    class Config:
        from_attributes = True

class AuthLibGetFull(AuthLibBase):
    id: int
    books: Optional[List['BookGet']] = None
    class Config:
        from_attributes = True

class AuthLibPut(AuthLibBase):
    id: int

class AuthLibPatch(BaseModel):
    id: int
    name: Optional[str] = None

class BookBase(BaseModel):
    title: str

class BookСreate(BookBase):
    author_id: int
    library_id: int

class BookGetFull(BookBase):
    id: int
    author: AuthLibGet
    library: AuthLibGet
    class Config:
        from_attributes = True

class BookGet(BookBase):
    id: int
    class Config:
        from_attributes = True

class BookPut(BookСreate):
    id: int

class BookPatch(BaseModel):
    id: int
    title: Optional[str] = None
    author_id: Optional[int] = None
    library_id: Optional[int] = None

class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T] = None
