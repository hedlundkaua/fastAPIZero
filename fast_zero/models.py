from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_as_dataclass, registry

table_registry = registry()

@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime]