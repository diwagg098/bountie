from db import Base
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP, 
    INTEGER
)
from sqlalchemy.orm import relationship

class Voucher(Base):
    __tablename__ = "vouchers"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT, nullable=False)
    start_date = Column("start_date", TIMESTAMP)
    end_date = Column("end_date", TIMESTAMP)
    amount = Column("amount", INTEGER)
    max_amount = Column("max_amount", INTEGER)
    created_at = Column("created_at", TIMESTAMP, server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP, server_default=text("now()"))

    promotion = relationship("Promotion")
