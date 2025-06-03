from sqlalchemy import (
    Column,
    Text,
    DateTime,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import registry


_USER_BASE_REPO = registry().generate_base()

class UserInfo(_USER_BASE_REPO):
    __tablename__ = "users"
    # should add index for user_id 
    email = Column(Text, primary_key=True, index=True)
    username = Column(Text)
    role = Column(Text)
    password = Column(Text)
    created_at = Column(DateTime(timezone=True), 
                        default=func.now())
    updated_at = Column(DateTime(timezone=True), 
                        default=func.now())
