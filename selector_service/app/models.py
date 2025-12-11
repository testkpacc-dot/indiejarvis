from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from .db import Base


class BanditArm(Base):
    __tablename__ = "bandit_arms"

    prompt_id = Column(String, primary_key=True, index=True)
    alpha = Column(Integer, nullable=False, default=1)
    beta = Column(Integer, nullable=False, default=1)
    samples = Column(Integer, nullable=False, default=0)
    risk = Column(String, nullable=False, default="low")  # "low" | "high"
    last_update = Column(DateTime, default=datetime.utcnow)
