from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

from pydantic import BaseModel

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(title="FastAPI Memo App")

# --- CORS設定 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React開発環境のURL
    allow_credentials=True,
    allow_methods=["*"],  # 全HTTPメソッド許可
    allow_headers=["*"],  # 全ヘッダー許可
)

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Welcome to Memo API"}

# タスク一覧の取得エンドポイント
@app.get("/memos/", response_model=List[schemas.MemoResponse])
def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # CRUDモジュールのget_todos関数を呼び出し
    memos = crud.get_memos(db, skip=skip, limit=limit)
    return memos

# 特定のタスクを取得するエンドポイント
# @app.get("/memos/{memo_id}", response_model=schemas.MemoResponse)
# def read_memo(memo_id: int, db: Session = Depends(get_db)):
#     # CRUDモジュールのget_memo関数を呼び出し
#     db_memo = crud.get_memo(db, memo_id=memo_id)
#     if db_memo is None:
#         # 見つからない場合は404エラー
#         raise HTTPException(status_code=404, detail="Memo not found")
#     return db_memo

# 新しいタスクを作成するエンドポイント
@app.post("/memos/", response_model=schemas.MemoResponse)
def create_memo(memo: schemas.MemoCreate, db: Session = Depends(get_db)):
    # CRUDモジュールのcreate_memo関数を呼び出し
    return crud.create_memo(db=db, memo=memo)

# タスクを更新するエンドポイント
@app.put("/memos/{memo_id}", response_model=schemas.MemoResponse)
def update_memo(memo_id: int, memo: schemas.MemoUpdate, db: Session = Depends(get_db)):
    # CRUDモジュールのupdate_memo関数を呼び出し
    db_memo = crud.update_memo(db=db, memo_id=memo_id, memo=memo)
    if db_memo is None:
        # 見つからない場合は404エラー
        raise HTTPException(status_code=404, detail="Memo not found")
    return db_memo

# タスクを削除するエンドポイント
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    # CRUDモジュールのdelete_todo関数を呼び出し
    success = crud.delete_memo(db=db, memo_id=memo_id)
    if not success:
        # 見つからない場合は404エラー
        raise HTTPException(status_code=404, detail="Memo not found")
    return {"message": "Memo deleted successfully"}