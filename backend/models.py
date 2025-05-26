from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base class for declarative models
Base = declarative_base()

class Student(Base):
    """Represents the students table in the database."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nid = Column(String, nullable=False)
    term = Column(String)
    gender = Column(String)
    phone1 = Column(String)
    phone2 = Column(String)
    # Note: The 'fees' column here might be intended for something else
    # as fees are stored in separate columns (fee1, fee2, etc.) in the database.py logic.
    # If this model is not actively used with the database.py functions,
    # consider if it's still needed or how it should be used.
    fees = Column(String)

# Database engine creation
# Connects to the students.db SQLite database.
# echo=True will print SQL statements to the console (useful for debugging).
engine = create_engine("sqlite:///students.db", echo=False) # Set echo to False for less verbose output

# Create tables defined by models
# This should ideally be called once during application setup (e.g., in init_db.py).
# Calling it here might overwrite tables if models.py is imported frequently.
# Consider if Base.metadata.create_all(engine) is needed here if init_db.py is used.
# Base.metadata.create_all(engine)

# Session factory creation
# Use this to create new Session objects to interact with the database.
SessionLocal = sessionmaker(bind=engine)
