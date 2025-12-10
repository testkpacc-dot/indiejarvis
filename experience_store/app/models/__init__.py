# Experience model
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from app.db import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(String, index=True)
    response = Column(String)
    reward = Column(Integer)  # 0 or 1
    is_verified = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
