# backend/models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nid = Column(String, nullable=False)
    term = Column(String)
    gender = Column(String)
    phone1 = Column(String)
    phone2 = Column(String)
    fees = Column(String)

# إنشاء قاعدة البيانات
engine = create_engine("sqlite:///students.db", echo=True)
Base.metadata.create_all(engine)

# Session
SessionLocal = sessionmaker(bind=engine)
