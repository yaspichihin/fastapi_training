from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime as dt

from models.base import Base


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[dt] = mapped_column(default=dt.utcnow, server_default=func.now())
    