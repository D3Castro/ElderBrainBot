from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.achievement import Achievement
from app.schemas.achievement import AchievementCreate, AchievementUpdate


class CRUDAchievement(CRUDBase[Achievement, AchievementCreate, AchievementUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AchievementCreate, owner_id: int
    ) -> Achievement:
        obj_in_data = jsonable_encoder(obj_in)
        print(obj_in_data)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Achievement, obj_in: Union[AchievementUpdate, Dict[str, Any]]
    ) -> Achievement:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_public(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Achievement]:
        return (
            db.query(self.model)
            .filter(self.model.public == True)
            .offset(skip)
            .limit(limit)
            .all()
        )


achievement = CRUDAchievement(Achievement)
