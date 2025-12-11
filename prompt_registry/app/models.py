from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from .db import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(String, unique=True, index=True, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    text = Column(Text, nullable=False)

    # FIX: metadata -> meta_json
    meta_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    file_path = Column(String, nullable=True)
