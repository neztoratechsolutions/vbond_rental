from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.property_type import PropertyType


router = APIRouter(
    prefix="/property-types",
    tags=["Property Types"]
)


# =========================================================
# SCHEMAS
# =========================================================

class PropertyTypeCreate(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class PropertyTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


# =========================================================
# CREATE
# =========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_property_type(
    data: PropertyTypeCreate,
    db: Session = Depends(get_db)
):
    # Check duplicate name
    existing_property_type = (
        db.query(PropertyType)
        .filter(PropertyType.name == data.name)
        .first()
    )

    if existing_property_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property type already exists"
        )

    property_type = PropertyType(
        name=data.name,
        description=data.description,
        is_active=data.is_active
    )

    db.add(property_type)
    db.commit()
    db.refresh(property_type)

    return {
        "status": 201,
        "message": "Property type created successfully",
        "data": {
            "id": property_type.id,
            "name": property_type.name,
            "description": property_type.description,
            "is_active": property_type.is_active,
            "created_at": property_type.created_at,
            "updated_at": property_type.updated_at
        }
    }


# =========================================================
# GET ALL
# =========================================================

@router.get("")
def get_all_property_types(
    db: Session = Depends(get_db)
):
    property_types = (
        db.query(PropertyType)
        .order_by(PropertyType.id.desc())
        .all()
    )

    return {
        "status": 200,
        "message": "Property types fetched successfully",
        "count": len(property_types),
        "data": [
            {
                "id": property_type.id,
                "name": property_type.name,
                "description": property_type.description,
                "is_active": property_type.is_active,
                "created_at": property_type.created_at,
                "updated_at": property_type.updated_at
            }
            for property_type in property_types
        ]
    }


# =========================================================
# GET BY ID
# =========================================================

@router.get("/{property_type_id}")
def get_property_type(
    property_type_id: int,
    db: Session = Depends(get_db)
):
    property_type = (
        db.query(PropertyType)
        .filter(PropertyType.id == property_type_id)
        .first()
    )

    if not property_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property type not found"
        )

    return {
        "status": 200,
        "message": "Property type fetched successfully",
        "data": {
            "id": property_type.id,
            "name": property_type.name,
            "description": property_type.description,
            "is_active": property_type.is_active,
            "created_at": property_type.created_at,
            "updated_at": property_type.updated_at
        }
    }


# =========================================================
# UPDATE
# =========================================================

@router.put("/{property_type_id}")
def update_property_type(
    property_type_id: int,
    data: PropertyTypeUpdate,
    db: Session = Depends(get_db)
):
    property_type = (
        db.query(PropertyType)
        .filter(PropertyType.id == property_type_id)
        .first()
    )

    if not property_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property type not found"
        )

    # Update name only if provided
    if data.name is not None:

        existing_property_type = (
            db.query(PropertyType)
            .filter(
                PropertyType.name == data.name,
                PropertyType.id != property_type_id
            )
            .first()
        )

        if existing_property_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property type name already exists"
            )

        property_type.name = data.name

    # Update description only if provided
    if data.description is not None:
        property_type.description = data.description

    # Update active status only if provided
    if data.is_active is not None:
        property_type.is_active = data.is_active

    db.commit()
    db.refresh(property_type)

    return {
        "status": 200,
        "message": "Property type updated successfully",
        "data": {
            "id": property_type.id,
            "name": property_type.name,
            "description": property_type.description,
            "is_active": property_type.is_active,
            "created_at": property_type.created_at,
            "updated_at": property_type.updated_at
        }
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/{property_type_id}")
def delete_property_type(
    property_type_id: int,
    db: Session = Depends(get_db)
):
    property_type = (
        db.query(PropertyType)
        .filter(PropertyType.id == property_type_id)
        .first()
    )

    if not property_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property type not found"
        )

    db.delete(property_type)
    db.commit()

    return {
        "status": 200,
        "message": "Property type deleted successfully"
    }