from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Achievement])
def read_achievements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve achievements.
    """
    if crud.user.is_superuser(current_user):
        achievements = crud.achievement.get_multi(db, skip=skip, limit=limit)
    else:
        achievements = crud.achievement.get_multi_by_public(
            db=db, skip=skip, limit=limit
        )
    return achievements


@router.post("/", response_model=schemas.Achievement)
def create_achievements(
    *,
    db: Session = Depends(deps.get_db),
    achievement_in: schemas.AchievementCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new achievement.
    """
    if achievement_in.achieved_by_id and not crud.user.get(db, id=achievement_in.achieved_by_id):
         raise HTTPException(status_code=400, detail="Invalid 'achieved_by_id'")
    achievement = crud.achievement.create_with_owner(db=db, obj_in=achievement_in, owner_id=current_user.id)
    return achievement


@router.put("/{id}", response_model=schemas.Achievement)
def update_achievement(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    achievement_in: schemas.AchievementUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an achievement.
    """
    achievement = crud.achievement.get(db=db, id=id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    if not crud.user.is_superuser(current_user) and (achievement.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    achievement = crud.achievement.update(db=db, db_obj=achievement, obj_in=achievement_in)
    return achievement


@router.get("/{id}", response_model=schemas.Achievement)
def read_achievement(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get achievement by ID.
    """
    achievement = crud.achievement.get(db=db, id=id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    if not crud.user.is_superuser(current_user) and (achievement.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return achievement


@router.delete("/{id}", response_model=schemas.Achievement)
def delete_achievement(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an achievement.
    """
    achievement = crud.achievement.get(db=db, id=id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    if not crud.user.is_superuser(current_user) and (achievement.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    achievement = crud.achievement.remove(db=db, id=id)
    return achievement
