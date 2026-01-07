from sqlalchemy import Column, Integer, String, Float, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class User(Base, TimestampMixin):
    __tablename__ = "User"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    name= Column(String, nullable= False)
    last_name= Column(String, nullable=False)
    balance =Column(Double, nullable=False, default=0)
    phone= Column(String, nullable=False)
    credit_debt = Column(Double, nullable=False, default=0)



class Feed(Base, TimestampMixin):
    __tablename__ = "Feed"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_pay_id = Column(Integer)
    user_paid_id = Column(Integer)
    ammount = Column(Double, nullable=False)
