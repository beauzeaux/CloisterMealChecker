import sqlalchemy
from sqlalchemy.types import Boolean, DateTime
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from datetime import datetime

DB = "sqlite:///cloister.db"
Base = declarative_base()
engine = create_engine(DB)
Session = sessionmaker(bind = engine)

# All people who swipe through the system
class Person(Base):
    __tablename__ = 'People'

    id       = Column(Integer, primary_key=True)
    first    = Column(String)
    last     = Column(String)
    email    = Column(String)      # this may need to be updated from the Princeton LDAP
    year     = Column(Integer)
    member   = Column(Boolean)
    prospect = Column(Boolean)
    maxGuest = Column(Integer)
    swipes   = relationship("Swipe", order_by="Swipe.id", backref="person")
    guestSwipes = relationship("GuestSwipe", backref="person")
    
    def __init__(self, id, first, last, email="", year="", member=False, prospect=False, maxGuest = 20):
        self.id       = id
        self.first    = first
        self.last     = last
        self.email    = email
        self.year     = year
        self.member   = member
        self.prospect = prospect

    def __repr__(self):
        return """<Person: {0}, {1}, {2}>""".format(self.first, self.last, self.id)
        
    def swipe(self, member = None):
        session = Session()
        if self.member:
            swipe = Swipe(self.id)
            session.add(swipe)
        elif member and member.member: # if there is guest swipe
            swipe = Swipe(self.id)
            session.add(swipe)
            session.commit()
            guestSwipe = GuestSwipe(member.id, swipe.id)
            session.add(guestSwipe)
        else:
            session.close()
            return False, "Not a valid member"

        session.commit()
        session.close()
        return True, ""

    """
    Swipes for special events (I.E. sophmore brunch
    """
    def eventSwipe(self):
        session = Session()
        swipe = Swipe(self.id)
        session.add(swipe)
        session.commit()
        session.close()

class Blacklist(Base):
    __tablename__ = "Blacklist"
    id     = Column(Integer, primary_key=True)
    pid    = Column(Integer, ForeignKey('People.id'))
    expire = Column(DateTime)   # expiration of the blacklist

    def __init__(self, pid, expire):
        this.pid = pid
        this.expire = expire    # should do error checking on this before using it

class Swipe(Base):
    __tablename__ = "Swipes"
    id     = Column(Integer, primary_key=True)
    pid    = Column(Integer, ForeignKey('People.id'))
    time   = Column(DateTime)
    def __init__(self, pid):
        self.pid = pid
        now = datetime.now()
        self.time = now

class GuestSwipe(Base):
    __tablename__ = "GuestSwipes"
    id     = Column(Integer, primary_key=True)
    mid    = Column(Integer, ForeignKey('People.id')) # the member id
    sid    = Column(Integer, ForeignKey('Swipes.id'))
    swipe  = relationship("Swipe", uselist=False)
    
    def __init__(self, mid, sid):
        self.mid = mid
        self.sid = sid

    def __repr__(self):
        member = self.person
        guest = self.swipe.person
        return "<GuestSwipe {0} {1}, {2} {3}>".format(member.first, member.last,
                                                  guest.first, guest.last)

def person_by_id(id):
    session = Session()
    person = session.query(Person).filter(Person.id==id).first()
    session.close()
    return person;
    
def init():
    Base.metadata.create_all(engine)

