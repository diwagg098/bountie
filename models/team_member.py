from tkinter.tix import Tree
from turtle import back
from db import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref

class TeamMember(Base):
    __tablename__ = "team_members"
    user_id = Column("user_id", ForeignKey("users.id"), primary_key=True)
    team_id = Column("team_id", ForeignKey("teams.id"), primary_key=True)
