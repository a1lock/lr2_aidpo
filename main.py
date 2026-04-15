from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, database

app = FastAPI(title="Grade Management System")

# Инициализация БД
models.Base.metadata.create_all(bind=database.engine)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Теперь Swagger будет отправлять данные правильно
    if form_data.username == "teacher" and form_data.password == "123":
        return {"access_token": auth.create_access_token({"sub": "teacher", "role": "Teacher"}), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect login or password")

@app.post("/grades/", response_model=schemas.GradeResponse)
def create_grade(
    grade: schemas.GradeCreate, 
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    # задание 3 Проверка прав доступа (только преподаватель)
    if current_user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # задание 2 CRUD создание записи
    new_grade = models.Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    
    # реализация требования 5 из ЛР1 автоматическое логирование
    log_entry = models.AuditLog(user_id=1, action=f"Created grade for student {grade.student_id}")
    db.add(log_entry)
    db.commit()
    
    return new_grade

@app.get("/grades/{student_id}")
def read_grades(student_id: int, db: Session = Depends(database.get_db)):
    # задание 2 CRUD чтение данных
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()