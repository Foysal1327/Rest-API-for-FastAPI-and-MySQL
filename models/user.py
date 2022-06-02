from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BIGINT, BOOLEAN, false, text

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(INTEGER, primary_key=True)
    first_name = Column(String(512), nullable=True)
    last_name = Column(String(512), nullable=True)
    deleted = (Column(BOOLEAN, default=False))
    created_by = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))