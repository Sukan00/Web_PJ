from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Annotated
from database import SessionLocal, engine
import json
import uvicorn
import shutil
import models
import schemas

app = FastAPI()

# Frontend เรียก API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตให้ทุก origin เรียก API ได้
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตให้ใช้ HTTP methods ทั้งหมด
    allow_headers=["*"],  # อนุญาตให้ใช้ headers ทั้งหมด
)

# สร้างตารางในฐานข้อมูล
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# CRUD User
@app.post("/User/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: db_dependency):
    # ตรวจสอบสิทธิ์การเข้าถึงเว็บ
    if not user.email.endswith("@kmitl.ac.th"):
        raise HTTPException(status_code=400, detail="Email must be @kmitl.ac.th")
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD Advisor
@app.post("/Advisor/", response_model=schemas.AdvisorResponse)
def create_advisor(advisor: schemas.AdvisorCreate, db: db_dependency):
    db_advisor = models.Advisor(**advisor.model_dump())
    db.add(db_advisor)
    db.commit()
    db.refresh(db_advisor)
    return db_advisor

# CRUD Report
@app.post("/Report/", response_model=schemas.ReportResponse)
def create_report(report: schemas.ReportCreate, db: db_dependency):
    # ตรวจสอบว่า user และ advisor มีอยู่ในระบบหรือไม่
    db_user = db.query(models.User).filter(models.User.email == report.creator).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_advisor = db.query(models.Advisor).filter(models.Advisor.email == report.advisor_email).first()
    if not db_advisor:
        raise HTTPException(status_code=404, detail="Advisor not found")

    # สร้างรายงาน
    db_report = models.Report(
        title=report.title,
        intro=report.intro,
        year=report.year,
        category=report.category,
        org=report.org,
        type_org=report.type_org,
        position=report.position,
        path=report.path,
        creator=report.creator,
        author=report.author,
        advisor_email=report.advisor_email
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # เพิ่มผู้จัดทำ
    for author_name in report.author:
        db_author = models.Author(name=author_name, report_id=db_report.report_id)
        db.add(db_author)

    # เพิ่มหมวดหมู่รายงาน
    for type_name in report.types:
        db_type = db.query(models.Type_Report).filter(models.Type_Report.name == type_name).first()
        if not db_type:
            db_type = models.Type_Report(name=type_name)
            db.add(db_type)
        db_report.types.append(db_type)

    db.commit()
    db.refresh(db_report)
    return db_report

# ดึงรายงานทั้งหมด
@app.get("/Report/", response_model=List[schemas.ReportResponse])
def get_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reports = db.query(models.Report).offset(skip).limit(limit).all()
    return reports

# อัปโหลดไฟล์รายงาน pdf
@app.post("/upload/")
async def upload_report(file: UploadFile = File(...)):

    file_path = "file.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            print(data)
    except FileNotFoundError:
        print(f"ไม่พบไฟล์ {file_path}")
    except json.JSONDecodeError:
        print(f"ไฟล์ {file_path} มีรูปแบบ JSON ไม่ถูกต้อง")

    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": file_location}

# AI Chatbot
@app.post("/chatbot/")
def chatbot_query(query: str):
    # Placeholder for AI chatbot logic
    return {"response": "This is a placeholder response from the AI chatbot."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
