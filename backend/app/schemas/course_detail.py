from pydantic import BaseModel


class LessonMini(BaseModel):
    id: int
    title: str
    lesson_order: int

    completed: bool
    locked: bool
    has_quiz: bool

    class Config:
        from_attributes = True

class ModuleDetail(BaseModel):
    id: int
    title: str
    description: str
    module_order: int
    lessons: list[LessonMini]

    class Config:
        from_attributes = True


class CourseDetail(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    difficulty: str

    modules: list[ModuleDetail]

    class Config:
        from_attributes = True