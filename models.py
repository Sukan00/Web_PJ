from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Relation table between Type Report with Report
report_type_association = Table(
    "report_type_association",
    Base.metadata,
    Column("report_id", Integer, ForeignKey("Report.report_id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("Type_Report.type_id"), primary_key=True),
)

# User table
class User(Base):
    __tablename__ = "User"

    email = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    reports = relationship("Report", back_populates="owner")

# Report table
class Report(Base):
    __tablename__ = "Report"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    intro = Column(String)
    year = Column(Integer)
    category = Column(String) # Co-op or Special project
    org = Column(String)
    type_org = Column(String)
    position = Column(String)
    path = Column(String)
    creator = Column(String, ForeignKey("User.email"), unique=True)
    author = Column(String)
    advisor_email = Column(String, ForeignKey("Advisor.email"), unique=True)

    owner = relationship("User", back_populates="reports")
    authors = relationship("Author", back_populates="report")
    advisor = relationship("Advisor", back_populates="reports")
    types = relationship("Type_Report", secondary=report_type_association, back_populates="reports")

# Type Report table
class Type_Report(Base):
    __tablename__ = "Type_Report"
    type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    reports = relationship("Report", secondary=report_type_association, back_populates="types")

# Advisor table
class Advisor(Base):
    __tablename__ = "Advisor"
    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    reports = relationship("Report", back_populates="advisor")

# Author table
class Author(Base):
    __tablename__ = "Author"
    au_id = Column(String, primary_key=True, index=True) # Student id
    name = Column(String)
    report_id = Column(Integer, ForeignKey("Report.report_id"), unique=True)
    report = relationship("Report", back_populates="authors")