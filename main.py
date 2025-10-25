
from fastapi import FastAPI, Query
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание приложения FastAPI
app = FastAPI(title="Student Performance System", description="API for tracking student grades")

# Настройка CORS для frontend на порту 8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["student_performance_db"]
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Модели для данных (Pydantic для валидации)
class Group(BaseModel):
    name: str

class Student(BaseModel):
    full_name: str
    group_id: str

class Teacher(BaseModel):
    full_name: str

class Course(BaseModel):
    name: str
    teacher_id: str

class Grade(BaseModel):
    student_id: str
    course_id: str
    grade: int

# Функция для конвертации ObjectId в str (для JSON)
def to_str(data):
    if isinstance(data, list):
        return [to_str(item) for item in data]
    if isinstance(data, dict):
        return {k: str(v) if isinstance(v, ObjectId) else to_str(v) for k, v in data.items()}
    return data

# Эндпоинты для групп
@app.post("/groups/")
def create_group(group: Group):
    result = db.groups.insert_one({"name": group.name})
    return {"id": str(result.inserted_id)}

@app.get("/groups/")
def get_groups():
    groups = list(db.groups.find())
    return to_str(groups)

# Эндпоинты для студентов
@app.post("/students/")
def create_student(student: Student):
    result = db.students.insert_one({
        "full_name": student.full_name,
        "group_id": ObjectId(student.group_id)
    })
    return {"id": str(result.inserted_id)}

@app.get("/students/")
def get_students(group_name: str = Query(None)):
    if group_name:
        # Частичное совпадение с regex, case-insensitive
        group_ids = [g["_id"] for g in db.groups.find({"name": {"$regex": group_name, "$options": "i"}})]
        query = {"group_id": {"$in": group_ids}}
    else:
        query = {}
    students = list(db.students.find(query))
    for s in students:
        group = db.groups.find_one({"_id": s["group_id"]})
        s["group_name"] = group["name"] if group else "Неизвестно"
    return to_str(students)

# Эндпоинты для преподавателей
@app.post("/teachers/")
def create_teacher(teacher: Teacher):
    result = db.teachers.insert_one({"full_name": teacher.full_name})
    return {"id": str(result.inserted_id)}

@app.get("/teachers/")
def get_teachers():
    teachers = list(db.teachers.find())
    return to_str(teachers)

# Эндпоинты для курсов
@app.post("/courses/")
def create_course(course: Course):
    result = db.courses.insert_one({
        "name": course.name,
        "teacher_id": ObjectId(course.teacher_id)
    })
    return {"id": str(result.inserted_id)}

@app.get("/courses/")
def get_courses():
    courses = list(db.courses.find())
    for c in courses:
        teacher = db.teachers.find_one({"_id": c["teacher_id"]})
        c["teacher_name"] = teacher["full_name"] if teacher else "Неизвестно"
    return to_str(courses)

# Эндпоинты для оценок
@app.post("/grades/")
def create_grade(grade: Grade):
    result = db.grades.insert_one({
        "student_id": ObjectId(grade.student_id),
        "course_id": ObjectId(grade.course_id),
        "grade": grade.grade
    })
    return {"id": str(result.inserted_id)}

@app.get("/grades/")
def get_grades(course_name: str = Query(None), student_name: str = Query(None)):
    query = {}
    if course_name:
        # Частичное совпадение с regex
        course_ids = [c["_id"] for c in db.courses.find({"name": {"$regex": course_name, "$options": "i"}})]
        query["course_id"] = {"$in": course_ids}
    if student_name:
        # Частичное совпадение с regex
        student_ids = [s["_id"] for s in db.students.find({"full_name": {"$regex": student_name, "$options": "i"}})]
        query["student_id"] = {"$in": student_ids}
    grades = list(db.grades.find(query))
    for g in grades:
        student = db.students.find_one({"_id": g["student_id"]})
        course = db.courses.find_one({"_id": g["course_id"]})
        g["student_name"] = student["full_name"] if student else "Неизвестно"
        g["course_name"] = course["name"] if course else "Неизвестно"
    return to_str(grades)

# Сводная таблица "Итоговая успеваемость" ( ФИО Студента, Название Курса, ФИО Преподавателя, Итоговая Оценка)
@app.get("/summary/")
def get_summary():
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student"}},
        {"$unwind": "$student"},
        {"$lookup": {"from": "courses", "localField": "course_id", "foreignField": "_id", "as": "course"}},
        {"$unwind": "$course"},
        {"$lookup": {"from": "teachers", "localField": "course.teacher_id", "foreignField": "_id", "as": "teacher"}},
        {"$unwind": "$teacher"},
        {"$project": {
            "student_name": "$student.full_name",
            "course_name": "$course.name",
            "teacher_name": "$teacher.full_name",
            "grade": "$grade"
        }}
    ]
    summary = list(db.grades.aggregate(pipeline))
    return to_str(summary)

# Средний балл по группам
@app.get("/average/")
def get_average():
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student"}},
        {"$unwind": "$student"},
        {"$group": {"_id": "$student.group_id", "avg_grade": {"$avg": "$grade"}}},
        {"$lookup": {"from": "groups", "localField": "_id", "foreignField": "_id", "as": "group"}},
        {"$unwind": "$group"},
        {"$project": {"group_name": "$group.name", "avg_grade": {"$round": ["$avg_grade", 2]}}}
    ]
    average = list(db.grades.aggregate(pipeline))
    return to_str(average)

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)