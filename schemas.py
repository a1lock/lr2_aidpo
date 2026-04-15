from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# схема для входа в систему (используется в эндпоинте /token)
class UserLogin(BaseModel):
    username: str
    password: str

# базовая схема для оценки (поля, которые нужны при создании)
class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    value: int
    is_absent: bool = False

# схема для создания оценки (наследует базу)
class GradeCreate(GradeBase):
    pass

# схема для ответа (то, что мы возвращаем пользователю)
# добавляем ID и дату, которые генерирует сама БД
class GradeResponse(GradeBase):
    id: int
    created_at: datetime

    class Config:
        # нужно чтобы Pydantic умел работать с моделями SQLAlchemy
        from_attributes = True