from sqlalchemy import Column, ForeignKey, Integer, String, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class User(Base, TimestampMixin):
    __tablename__ = "User"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    balance = Column(Double, nullable=False, default=0)
    phone = Column(String(10), nullable=False)
    credit_debt = Column(Double, nullable=False, default=0)
    
    transactions_sent = relationship('Transaction', foreign_keys='Transaction.payer_id', backref='payer')
    transactions_received = relationship('Transaction', foreign_keys='Transaction.payee_id', backref='payee')

class Transaction(Base, TimestampMixin):
    __tablename__ = "Transaction"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    payer_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    payee_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    amount = Column(Double, nullable=False)
    description = Column(String(100), nullable=True)  
    balance_used = Column(Double, nullable=False)  
    credit_used = Column(Double, nullable=False, default=0)  
    

class Feed(Base, TimestampMixin):
    __tablename__ = "Feed"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    feed_type = Column(String(15), nullable=False)  # "payment" or "friend_add"
    
    transaction_id = Column(Integer, ForeignKey('Transaction.id'), nullable=True)
    
    payer_id = Column(Integer, ForeignKey('User.id'), nullable=True)
    payee_id = Column(Integer, ForeignKey('User.id'), nullable=True)
    
    transaction = relationship('Transaction', backref='feed_entries')
    payer_id = relationship('User', foreign_keys=[payer_id])
    payee_id = relationship('User', foreign_keys=[payee_id])