from db import Base
from sqlalchemy import Column, text, ForeignKey
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    INTEGER,
    TIMESTAMP,
    BOOLEAN
)
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT)
    username = Column("username", TEXT)
    password = Column("password", TEXT)
    fail_login = Column("fail_login", INTEGER, server_default="0")
    email = Column("email", TEXT, nullable=False, unique=True)
    phone = Column("phone", TEXT, unique=True)
    registration_date = Column("registration_date", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    last_login = Column("last_login", TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()"))
    dob = Column("dob", TIMESTAMP(timezone=True))
    country_code = Column("country_code", TEXT, ForeignKey("countries.code"), nullable=False)
    is_admin = Column("is_admin", BOOLEAN, server_default="f")
    bio = Column("bio", TEXT)
    photo_url = Column("photo_url", TEXT)

    teams = relationship('Team', secondary='team_members')

