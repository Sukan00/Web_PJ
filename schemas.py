from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    email: EmailStr # ตรวจสอบว่า email มีรูปแบบถูกต้องไหม
    password: str
    role: str

# สร้างคลาสใหม่เพื่อเตรียมพร้อมสำหรับการเพิ่ม att หรือ def ในอนาคต
class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    password: str
    role: str

    class Config:
        # อนุญาตให้แปลงข้อมูลจาก ORM objects เป็น Pydantic models
        from_attributes = True  

##############################################
class AdvisorBase(BaseModel):
    email: EmailStr
    name: str

class AdvisorCreate(AdvisorBase):
    pass

class AdvisorResponse(BaseModel):
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

##############################################
class ReportBase(BaseModel):
    title: str
    intro: str
    year: int
    category: str
    org: str
    type_org: str
    position: str
    path: str
    creator: EmailStr
    advisor_email: EmailStr
    author: List[str]
    types: List[str]

class ReportCreate(ReportBase):
    pass

class ReportResponse(BaseModel):
    title: str
    intro: str
    year: int
    category: str
    org: str
    type_org: str
    position: str
    path: str
    creator: EmailStr
    advisor_email: EmailStr
    author: List[str]
    types: List[str]

    class Config:
        from_attributes = True