from db import Base
from sqlalchemy import Column, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import (
    TEXT,
    UUID,
    TIMESTAMP,
    INTEGER
)

class Token(Base):
    __tablename__ = "tokens"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    symbol = Column("symbol", TEXT)

class P2PListing(Base):
    __tablename__ = "p2p_listings"
    id = Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    price = Column("price", INTEGER)
    max_amount = Column("max_amount", INTEGER)
    payment_method = Column("payment_method", TEXT)
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=func.now())
    agent_id = Column("agent_id", UUID, ForeignKey("p2p_agents.id"), nullable=False)
    token_symbol = Column("token_symbol", UUID, ForeignKey("tokens.symbol"), nullable=False)