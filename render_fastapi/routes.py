from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import *

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/book", response_model=List[BookGetFull])
async def get_book_service(db: Session = Depends(get_db)):
    res = crud.get_books(db)
    return res
@router.post("/book")
async def create_book_service(request: BookСreate, db: Session = Depends(get_db)):
    crud.create_book(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Book created successfully").model_dump(exclude_none=True)

@router.put("/book")
async def put_book_service(request: BookPut, db: Session = Depends(get_db)):
    crud.put_book(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Book put successfull").model_dump(exclude_none=True)

@router.patch("/book")
async def patch_book_service(request: BookPatch, db: Session = Depends(get_db)):
    crud.patch_book(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Book patch successfull").model_dump(exclude_none=True)

@router.delete("/book/{id}")
async def delete_book_service(id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, id)
    return Response(status="Ok",
                    code="200",
                    message="Book deleted successfully").model_dump(exclude_none=True)

@router.get("/library", response_model=List[AuthLibGetFull])
async def get_library_service(db: Session = Depends(get_db)):
    return crud.get_libraries(db)

@router.post("/library")
async def create_library_service(request: AuthLibBase, db: Session = Depends(get_db)):
    crud.create_library(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Library created successfully").model_dump(exclude_none=True)

@router.put("/library")
async def put_library_service(request: AuthLibPut, db: Session = Depends(get_db)):
    crud.put_library(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Library put successfull").model_dump(exclude_none=True)

@router.patch("/library")
async def patch_library_service(request: AuthLibPatch, db: Session = Depends(get_db)):
    crud.patch_library(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Library patch successfull").model_dump(exclude_none=True)

@router.delete("/library/{id}")
async def delete_library_service(id: int, db: Session = Depends(get_db)):
    crud.delete_library(db, id)
    return Response(status="Ok",
                    code="200",
                    message="Library deleted successfully").model_dump(exclude_none=True)

@router.get("/author", response_model=List[AuthLibGetFull])
async def get_author_service(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@router.post("/author")
async def create_author_service(request: AuthLibBase, db: Session = Depends(get_db)):
    crud.create_author(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Author created successfully").model_dump(exclude_none=True)

@router.put("/author")
async def put_author_service(request: AuthLibPut, db: Session = Depends(get_db)):
    crud.put_author(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Library put successfull").model_dump(exclude_none=True)
@router.patch("/author")
async def patch_author_service(request: AuthLibPatch, db: Session = Depends(get_db)):
    crud.patch_author(db, request)
    return Response(status="Ok",
                    code="200",
                    message="Library patch successfull").model_dump(exclude_none=True)
@router.delete("/author/{id}")
async def delete_author_service(id: int, db: Session = Depends(get_db)):
    crud.delete_author(db, id)
    return Response(status="Ok",
                    code="200",
                    message="Library deleted successfully").model_dump(exclude_none=True)