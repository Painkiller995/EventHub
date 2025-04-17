from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app import bcrypt, db


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    is_verified = Column(Boolean, default=False)

    # Relationships
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash the password and store it in the database."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Check the hashed password against the provided password."""
        return bcrypt.check_password_hash(self.password, password)


class Event(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=False)

    image_url = Column(String(255), default="/static/img/default_event_image.jpg")

    # Relationships
    user = relationship("User", back_populates="events")
    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")


class Registration(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
