from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from .db import Base


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    context = Column(Text, nullable=False)          # JSON string
    prompt_id = Column(String, index=True)
    response = Column(Text, nullable=False)         # JSON string
    trace = Column(Text, nullable=True)
    verifier_result = Column(Text, nullable=False)  # JSON string
    feedback = Column(Text, nullable=True)          # JSON string
