from backend.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import UUID, uuid4
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'
    # SQLAlchemyの機能により、SQLiteの場合: CHAR(32) 型のカラムが作成され、
    # UUIDはハイフンなしの32文字の文字列として保存されます。
    id: Mapped[UUID] = mapped_column(db.Uuid(), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(db.String(30), unique=True)
    email: Mapped[str] = mapped_column(db.String(256), unique=True)
    password: Mapped[str] = mapped_column(db.String(256))
    is_admin: Mapped[bool] = mapped_column(db.Boolean(), default=False)
    tokens_valid_from: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User id:{self.id}, username:"{self.username}", email:"{self.email}">'

    @classmethod
    def create_password_hash(cls, raw_password: str) -> str:
        return generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)



class TokenBlocklist(db.Model):
    __tablename__ = 'blocked_tokens'
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    jti: Mapped[str] = mapped_column(db.String(36), index=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Token jti:{self.jti}, created_at:{self.created_at}>"
