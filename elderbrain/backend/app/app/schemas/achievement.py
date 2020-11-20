from typing import Optional

from pydantic import BaseModel


# Shared properties
class AchievementBase(BaseModel):
    description: Optional[str] = None
    achieved_by_id: Optional[int] = None
    public: Optional[bool] = True


# Properties to receive on Achievement creation
class AchievementCreate(AchievementBase):
    description: str


# Properties to receive on Achievement update
class AchievementUpdate(AchievementBase):
    pass


# Properties shared by models stored in DB
class AchievementInDBBase(AchievementBase):
    id: int
    description: str
    owner_id: int
    public: bool = True

    class Config:
        orm_mode = True


# Properties to return to client
class Achievement(AchievementInDBBase):
    pass


# Properties properties stored in DB
class AchievementInDB(AchievementInDBBase):
    pass
