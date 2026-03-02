from datetime import datetime
from sqlalchemy import DECIMAL, Boolean, CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column


class Base(declarative_base()):
    __abstract__ = True


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(Text, default='')
    rating: Mapped[float] = mapped_column(DECIMAL(3, 2), CheckConstraint('rating >= 0 AND rating <= 5'), default=0)
    balance: Mapped[float] = mapped_column(DECIMAL(12, 2), default=0)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_freelancer: Mapped[bool] = mapped_column(Boolean, default=False)
    is_client: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, index=True, nullable=False)
    projects_posted: Mapped[int] = mapped_column(default=0)
    succes_rate: Mapped[float] = mapped_column(DECIMAL(5,2), CheckConstraint('succes_rate >= 0 AND succes_rate <= 100'), default=0)
    hires_count: Mapped[int] = mapped_column(default=0)
    active_projects: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(10), default='active')


class Freelancer(Base):
    __tablename__ = 'freelancers'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, index=True, nullable=False)
    succes_rate: Mapped[float] = mapped_column(DECIMAL(5,2), CheckConstraint('succes_rate >= 0 AND succes_rate <= 100'), default=0)
    completed_projects: Mapped[int] = mapped_column(default=0)
    reviews_count: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(10), default='active')


class  Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    tasks_count: Mapped[int] = mapped_column(default=0)


class Tasks(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(ForeignKey('freelancers.id'), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    full_text: Mapped[str] = mapped_column(Text, nullable=False)
    price_min: Mapped[float] = mapped_column(DECIMAL(12,2), CheckConstraint('price_min >= 0'), nullable=False)
    price_max: Mapped[float] = mapped_column(DECIMAL(12, 2), CheckConstraint('price_max >= 0'), nullable=False)
    deadline: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='open')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Transactions(Base):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    related_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), CheckConstraint('amount >= 0'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    