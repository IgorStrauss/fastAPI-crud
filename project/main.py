from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from project.models import Course
from project.database import engine, Base, get_db
from project.repositories import CourseRepository
from project.schemas import CourseRequest, CourseResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create(request: CourseRequest, db: Session = Depends(get_db)):
    curso = CourseRepository.save(db, Course(**request.dict()))
    return CourseRequest.from_orm(curso)


@app.get("/api/courses", response_model=List[CourseResponse])
def find_all(db: Session = Depends(get_db)):
    courses = CourseRepository.find_all(db)
    return [CourseResponse.from_orm(course) for course in courses]


@app.get("/api/courses/{id}", response_model=CourseResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    course = CourseRepository.find_by_id(db, id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    return CourseResponse.from_orm(course)


@app.delete("/api/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not CourseRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    CourseRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/api/courses/{id}", response_model=CourseResponse)
def update(id: int, request: CourseRequest, db: Session = Depends(get_db)):
    if not CourseRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    curso = CourseRepository.save(db, Course(id=id, **request.dict()))
    return CourseResponse.from_orm(curso)
