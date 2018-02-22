import sqlalchemy
print(sqlalchemy.__version__)

from sqlalchemy import create_engine

# Create in memory sqlite db, echo generated sql
engine = create_engine('sqlite:///', echo=True)

# Declarative base class
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


# Create a User class to map a sql table to
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return f'<User(name={self.name},\
        fullname={self.fullname},\
        password={self.password})'

    @property
    def serialize(self):
        return {
            'name': self.name,
            'fullname': self.fullname,
            'password': self.password
        }


Base.metadata.create_all(engine)


# Descriptions vs Full Descriptions
# Primary key requires a sql sequence, firebird Oracle db
'''
from sqlalchemy import Sequence

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50)) # specific len of string
    password = Column(String(12))

    def __repr__(self):
        return f'<User(name={self.name},\
        fullname={self.fullname},\
        password={self.password})'
'''

# Test user object

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name)
print(ed_user.fullname)
print(ed_user.password)
print(str(ed_user.id))  # returns None
print(ed_user.serialize)

# Create session to talk with the db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
