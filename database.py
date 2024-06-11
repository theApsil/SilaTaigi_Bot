from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bot.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    bonus_count = Column(Integer, default=0)
    gift_count = Column(Integer, default=0)
    service_code = Column(String)
    gift_code = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
