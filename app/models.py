from uuid import uuid4

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from .db.base import Base


class Post(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    body = Column(Text)
