from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Achievement(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    public = Column(Boolean, index=True)
    achieved_by_id = Column(Integer, ForeignKey("user.id"))
    owner_id = Column(Integer, ForeignKey("user.id"))
    achieve_owner = relationship("User", foreign_keys=[achieved_by_id], back_populates="achievements")
    create_owner = relationship("User", foreign_keys=[owner_id], back_populates="created_achievements")
