from sqlalchemy import Column, Integer, String, Float, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    name= Column(String, nullable= False)
    last_name= Column(String, nullable=False)
    balance =Column(Double, nullable=False, default=0)
    phone= Column(String, nullable=False)
    credit_debt = Column(Double, nullable=False, default=0)



class Feed(Base):
    __tablename__ = "Feed"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_pay_id = Column(Integer)
    user_paid_id = Column(Integer)
    ammount = Column()
