from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

# メモのデータモデル
class Memo(Base):
   __tablename__ = "memos"

   id = Column(Integer, primary_key=True, index=True)
   title = Column(String(100), nullable=False)
   content = Column(String(255))
   status = Column(String(50))
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())