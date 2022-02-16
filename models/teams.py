from db import Base
from sqlalchemy import Column, text, func
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "teams"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT, nullable=False)
    logo_url = Column("logo_url", TEXT)
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=func.now())
    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    members = relationship("User", secondary="team_members", overlaps="teams")
