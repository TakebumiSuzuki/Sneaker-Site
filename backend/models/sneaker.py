from sqlalchemy.orm import Mapped, mapped_column
from backend.extensions import db

from decimal import Decimal
from datetime import datetime, timezone
from backend.enums import CategoryEnum


class Sneaker(db.Model):
    __tablename__ = 'sneakers'

    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))
    description: Mapped[str] = mapped_column(db.String(1000), default='')
    category: Mapped[CategoryEnum] = mapped_column(db.Enum(CategoryEnum, native_enum=False), index=True)
    price: Mapped[Decimal|None] = mapped_column(db.Numeric(10, 2), index=True)
    stock: Mapped[int|None] = mapped_column(db.Integer())
    featured: Mapped[bool] = mapped_column(db.Boolean(), default=False)
    image_filename: Mapped[str|None] = mapped_column(db.String(256))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<Sneaker id:{self.id}, name:"{self.name}", stock:{self.stock}>'
