from db import Base
from sqlalchemy import Column, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP, 
    INTEGER
)
from sqlalchemy.orm import relationship

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", TEXT, nullable=False)
    start_date = Column("start_date", TIMESTAMP)
    end_date = Column("end_date", TIMESTAMP)
    banner_url = Column("banner_url", TEXT)
    tnc = Column("tnc", TEXT)
    created_at = Column("created_at", TIMESTAMP, server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP, server_default=text("now()"))

    voucher = Column("voucher_id", UUID(), ForeignKey("vouchers.id"))
