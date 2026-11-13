from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

# タスク一覧を取得
def get_memos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Memo]:
    return db.query(models.Memo).offset(skip).limit(limit).all()

# IDを指定して単一のタスクを取得
def get_memo(db: Session, memo_id: int) -> Optional[models.Memo]:
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()

# 新しいタスクをデータベースに追加
def create_memo(db: Session, memo: schemas.TodoCreate) -> models.Memo:
    db_memo = models.Memo(**memo.dict())
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

#  既存タスクの情報を更新
def update_memo(db: Session, memo_id: int, memo: schemas.MemoUpdate) -> Optional[models.Memo]:
    db_memo = get_memo(db, memo_id)
    if db_memo:
        update_data = memo.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_memo, key, value)
        db.commit()
        db.refresh(db_memo)
    return db_memo

# タスクをデータベースから削除
def delete_memo(db: Session, memo_id: int) -> bool:
    db_memo = get_memo(db, memo_id)
    if db_memo:
        db.delete(db_memo)
        db.commit()
        return True
    return False