from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(255))
    status = Column(String(50), default="active")
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    # expires_at = Column(DateTime)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    provider = Column(String(50),nullable=True )
    provider_id = Column(String(255),nullable=True )

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(String(255))
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    age = Column(Integer)
    passport = Column(String(255))
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    amount = Column(Integer)

    reference = Column(String(255))
    provider = Column(String(50))

    status = Column(String(50))
    
class OTP(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    otp = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer,primary_key=True,index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )