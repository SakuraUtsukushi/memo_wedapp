from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# メモの作成時に使用するスキーマ
class MemoCreate(BaseModel):
    title: str
    content: Optional[str] = None
    status: str

# メモの更新時に使用するスキーマ
class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: str

# メモの読み取り時に使用するスキーマ
class MemoResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
