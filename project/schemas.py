from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: str
    workload: int


class CourseRequest(CourseBase):
    ...

    class Config:
        orm_mode = True


class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True
