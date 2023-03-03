from sqlalchemy.orm import Session
from typing import List
from project.models import Course


class CourseRepository:
    @staticmethod
    def find_all(db: Session) -> List[Course]:
        return db.query(Course).all()

    @staticmethod
    def save(db: Session, course: Course) -> Course:
        if course.id:
            db.merge(course)
        else:
            db.add(course)
        db.commit()
        return course

    @staticmethod
    def find_by_id(db: Session, id: int) -> Course:
        return db.query(Course).filter(Course.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Course).filter(Course.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        course = db.query(Course).filter(Course.id == id).first()
        if course is not None:
            db.delete(course)
            db.commit()
