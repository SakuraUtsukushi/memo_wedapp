from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# アプリケーションとデータベースの橋渡し
# .envファイルから環境変数を読み込む
load_dotenv()

# データベースURLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemyのエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションクラスを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのBaseクラスを作成
Base = declarative_base()

# DBセッションを取得するための関数を定義
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()
