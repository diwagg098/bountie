from db import Base
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID
)

class Country(Base):
    __tablename__ = "countries"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    code = Column("code", TEXT, nullable=False, unique=True)
    name = Column("name", TEXT)
    phone_code = Column("phone_code", TEXT)
