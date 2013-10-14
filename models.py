from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base, db_session
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    access_token = Column(String(100))
    username = Column(String(50))
    facebook_id = Column(String(50))
    facebook_url = Column(String(100))
    is_admin = Column(Boolean(), default=False)
    markers = relationship("Marker", backref="user")

    def serialize(self):
        return {
            "id" : str(self.key()),
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "username" : self.username,
            "facebook_id" : self.facebook_id,
            "facebook_url" : self.facebook_url,
            "is_admin" : self.is_admin,
        }

class Marker(Base):
    __tablename__ = "markers"

    MARKER_TYPE_ACCIDENT = 1
    MARKER_TYPE_HAZARD = 2
    MARKER_TYPE_OFFER = 3
    MARKER_TYPE_PLEDGE = 4
    MARKER_TYPE_BILL = 5
    MARKER_TYPE_ENGINEERING_PLAN = 6
    MARKER_TYPE_CITY = 7
    MARKER_TYPE_OR_YAROK = 8

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("user.id"))
    title = Column(String(100))
    description = Column(String)
    type = Column(Integer)
    subtype = Column(Integer)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    latitude = Column(Float())
    longitude = Column(Float())
    address = Column(String)

    def serialize(self, current_user):
        return {
            "id" : str(self.key()),
            "title" : self.title,
            "description" : self.description,
            "address" : self.address,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "type" : self.type,

            # TODO: fix relationship
            "user" : self.user.serialize(),

            # TODO: fix query
            "followers" : [x.user.serialize() for x in Follower.all().filter("marker", self).fetch(100)],

            # TODO: fix query
            "following" : Follower.all().filter("user", current_user).filter("marker", self).filter("user", current_user).get() is not None if current_user else None,
            "created" : self.created.isoformat(),
        }

    def update(self, data, current_user):
        self.title = data["title"]
        self.description = data["description"]
        self.type = data["type"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]

        follower = db_session.query(Follower).filter(Follower.marker == self.id).filter(Follower.user == current_user).get(1)

        if data["following"]:
            if not follower:
                Follower(marker = self.id, user = current_user)
        else:
            if follower:
                follower[0].delete()

        self.put()

    @classmethod
    def bounding_box_fetch(cls, ne_lat, ne_lng, sw_lat, sw_lng):
        # TODO: implement query
        pass

    @classmethod
    def parse(cls, data):
        return Marker(
            title = data["title"],
            description = data["description"],
            type = data["type"],
            latitude = data["latitude"],
            longitude = data["longitude"]
        )

class Follower(Base):
    __tablename__ = "followers"
    
    user = Column(Integer, ForeignKey("user.id"), primary_key=True)
    marker = Column(Integer, ForeignKey("marker.id"), primary_key=True)
