from db import Base
from sqlalchemy import Column, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP, 
    BOOLEAN
)

class P2PAgent(Base):
    __tablename__ = "p2p_agents"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT, nullable=False)
    phone = Column("phone", TEXT, unique=True)
    telegram = Column("telegram", TEXT, unique=True)
    active = Column("active", BOOLEAN, server_default="t")
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=func.now())
    country_code = Column("country_code", TEXT, ForeignKey("countries.code"), nullable=False)