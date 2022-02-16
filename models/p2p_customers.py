from db import Base
from sqlalchemy import Column, text, func
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP
)


class P2PCust(Base):
    __tablename__ = "p2p_customers"
    id = Column("id", UUID(as_uuid=True), primary_key=True,
                server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT, nullable=False)
    phone = Column("phone", TEXT, unique=True)
    email = Column("email", TEXT, unique=True)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP(
        timezone=True), server_default=text("now()"), onupdate=func.now())
