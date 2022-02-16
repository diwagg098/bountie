from db import Base
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    BOOLEAN
)


class Game(Base):
    __tablename__ = "games"
    id = Column("id", UUID(as_uuid=True), primary_key=True,
                server_default=text("uuid_generate_v4()"))
    image_url = Column("image_url", TEXT, nullable=False, unique=True)
    name = Column("name", TEXT)
    description = Column("description", TEXT)
    featured = Column('featured', BOOLEAN)
