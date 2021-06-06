# import os

from sqlalchemy import Column
from sqlalchemy.types import String, Integer, DateTime, Boolean
# from sqlalchemy.types import Text, JSON, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from datetime import datetime  # , timedelta

Base = declarative_base()


class MockTable(Base):
    __tablename__ = "mock_table"

    id = Column(Integer, primary_key=True)
    uniqueString = Column(String, unique=True)
    integer = Column(Integer, unique=True)
    boolean = Column(Boolean, unique=True)
    create_at = Column(DateTime, default=datetime.utcnow)
