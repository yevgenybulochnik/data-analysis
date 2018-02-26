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
        return f'<User(name={self.name}, fullname={self.fullname}, password={self.password})>'

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

# from sqlalchemy import Sequence

# class User(Base):
    # __tablename__ = 'users'

    # id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    # name = Column(String(50))
    # fullname = Column(String(50)) # specific len of string
    # password = Column(String(12))

    # def __repr__(self):
        # return f'<User(name={self.name},\
        # fullname={self.fullname},\
        # password={self.password})'

# Test user object

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name)
print(ed_user.fullname)
print(ed_user.password)
print(str(ed_user.id))  # returns None as data has not been commited to db
print(ed_user.serialize)

# Create session to talk with the db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Persist ed_user object, add to db
session.add(ed_user)  # no entry created yet, data needs to be flushed

# Query or user ed, this will flush data then query the db
our_user = session.query(User).filter_by(name='ed').first()

# our_user and ed_user reference the same object and row in the db
print(our_user is ed_user)  # True

# Add more users
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')
])

# Change the password for ed
ed_user.password = 'f8s7ccs'

# Session knows when data has been change, like ed_user's password
print(session.dirty)

# Session also know that three new objects are pending
print(session.new)

# Commit changes to db including INSERT on new users and UPDATE on ed
session.commit()

# commit flushes changes to db and commits transactions
# ed_user id is now set to 1 instead of None
print(ed_user.id)

# Rollback changes within a session
ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)
session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

# Rollback above changes
session.rollback()
print(ed_user.name)  # u'ed'
print(fake_user in session)  # False

# Querying
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

# Use the User table class to get itmes
for row in session.query(User, User.name).all():
    print(row.User, row.name)

# Relabel a column expresssion
for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

# Relabel table/class name
from sqlalchemy.orm import aliased

user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)

# Limit a query
for u in session.query(User).order_by(User.id)[1:3]:
    print(u)

# Filter query
for name, in session.query(User.name).filter_by(fullname='Ed Jones'):  # comma needed to git single result
    print(name)

# Filter function
for name, in session.query(User.name).filter(User.fullname == 'Ed Jones'):
    print(name)

# Chained filters, work like AND
for user in session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones'):
    print(user)

# Common filter operators

# like, case-insensitive on some backends and not others, ilike is case-insensitive
for user in session.query(User).filter(User.name.like('%ed%')):
    print(user.name)

# in filter
for user in session.query(User).filter(User.name.in_(['ed', 'wendy', 'jack'])):
    print(user.name)

for user in session.query(User).filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%')))):
    print(user.name)
