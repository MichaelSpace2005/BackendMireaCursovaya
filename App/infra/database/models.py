from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    email_tokens = relationship("EmailTokenDB", back_populates="user", cascade="all, delete-orphan")

class EmailTokenDB(Base):
    __tablename__ = "email_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    
    user = relationship("UserDB", back_populates="email_tokens")

class MechanicDB(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)

    outgoing = relationship("LinkDB", back_populates="from_mechanic", foreign_keys="LinkDB.from_id")
    incoming = relationship("LinkDB", back_populates="to_mechanic", foreign_keys="LinkDB.to_id")

class LinkDB(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False)
    to_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False)
    type = Column(String(50), nullable=False)

    from_mechanic = relationship("MechanicDB", foreign_keys=[from_id], back_populates="outgoing")
    to_mechanic = relationship("MechanicDB", foreign_keys=[to_id], back_populates="incoming")