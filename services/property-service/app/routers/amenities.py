from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.amenity import Amenity
from typing import Optional


router = APIRouter(
    prefix="/amenities",
    tags=["Amenities"]
)


# =========================================================
# SCHEMAS
# =========================================================

class AmenityCreate(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True



class AmenityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# =========================================================
# CREATE
# =========================================================

@router.post("", status_code=status.HTTP_201_CREATED)
def create_amenity(
    data: AmenityCreate,
    db: Session = Depends(get_db)
):
    existing_amenity = (
        db.query(Amenity)
        .filter(Amenity.name == data.name)
        .first()
    )

    if existing_amenity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amenity already exists"
        )

    amenity = Amenity(
        name=data.name,
        description=data.description,
        is_active=data.is_active
    )

    db.add(amenity)
    db.commit()
    db.refresh(amenity)

    return {
        "status": 201,
        "message": "Amenity created successfully",
        "data": {
            "id": amenity.id,
            "name": amenity.name,
            "description": amenity.description,
            "is_active": amenity.is_active,
            "created_at": amenity.created_at,
            "updated_at": amenity.updated_at
        }
    }


# =========================================================
# GET ALL
# =========================================================

@router.get("")
def get_all_amenities(
    db: Session = Depends(get_db)
):
    amenities = (
        db.query(Amenity)
        .order_by(Amenity.id.desc())
        .all()
    )

    return {
        "status": 200,
        "message": "Amenities fetched successfully",
        "count": len(amenities),
        "data": [
            {
                "id": amenity.id,
                "name": amenity.name,
                "description": amenity.description,
                "is_active": amenity.is_active,
                "created_at": amenity.created_at,
                "updated_at": amenity.updated_at
            }
            for amenity in amenities
        ]
    }


# =========================================================
# GET BY ID
# =========================================================

@router.get("/{amenity_id}")
def get_amenity(
    amenity_id: int,
    db: Session = Depends(get_db)
):
    amenity = (
        db.query(Amenity)
        .filter(Amenity.id == amenity_id)
        .first()
    )

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found"
        )

    return {
        "status": 200,
        "message": "Amenity fetched successfully",
        "data": {
            "id": amenity.id,
            "name": amenity.name,
            "description": amenity.description,
            "is_active": amenity.is_active,
            "created_at": amenity.created_at,
            "updated_at": amenity.updated_at
        }
    }


# =========================================================
# UPDATE
# =========================================================

@router.put("/{amenity_id}")
def update_amenity(
    amenity_id: int,
    data: AmenityUpdate,
    db: Session = Depends(get_db)
):
    amenity = (
        db.query(Amenity)
        .filter(Amenity.id == amenity_id)
        .first()
    )

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found"
        )

    # Update name only if provided
    if data.name is not None:

        existing_amenity = (
            db.query(Amenity)
            .filter(
                Amenity.name == data.name,
                Amenity.id != amenity_id
            )
            .first()
        )

        if existing_amenity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amenity name already exists"
            )

        amenity.name = data.name

    # Update description only if provided
    if data.description is not None:
        amenity.description = data.description

    # Update active status only if provided
    if data.is_active is not None:
        amenity.is_active = data.is_active

    db.commit()
    db.refresh(amenity)

    return {
        "status": 200,
        "message": "Amenity updated successfully",
        "data": {
            "id": amenity.id,
            "name": amenity.name,
            "description": amenity.description,
            "is_active": amenity.is_active,
            "created_at": amenity.created_at,
            "updated_at": amenity.updated_at
        }
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/{amenity_id}")
def delete_amenity(
    amenity_id: int,
    db: Session = Depends(get_db)
):
    amenity = (
        db.query(Amenity)
        .filter(Amenity.id == amenity_id)
        .first()
    )

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found"
        )

    db.delete(amenity)
    db.commit()

    return {
        "status": 200,
        "message": "Amenity deleted successfully"
    }