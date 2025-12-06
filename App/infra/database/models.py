from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class MechanicDB(Base):
    """Database model for GameMechanic"""
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)

    # Relationships
    outgoing = relationship(
        "LinkDB",
        back_populates="from_mechanic",
        foreign_keys="LinkDB.from_id",
        cascade="all, delete-orphan"
    )
    incoming = relationship(
        "LinkDB",
        back_populates="to_mechanic",
        foreign_keys="LinkDB.to_id"
    )


class LinkDB(Base):
    """Database model for EvolutionLink"""
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, ForeignKey("mechanics.id", ondelete="CASCADE"), nullable=False)
    to_id = Column(Integer, ForeignKey("mechanics.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)

    # Relationships
    from_mechanic = relationship(
        "MechanicDB",
        foreign_keys=[from_id],
        back_populates="outgoing"
    )
    to_mechanic = relationship(
        "MechanicDB",
        foreign_keys=[to_id],
        back_populates="incoming"
    )


class UserDB(Base):
    """Database model for User"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tokens = relationship("EmailTokenDB", back_populates="user", cascade="all, delete-orphan")


class EmailTokenDB(Base):
    """Database model for email verification token"""
    __tablename__ = "email_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_used = Column(Boolean, default=False)

    user = relationship("UserDB", back_populates="tokens")
