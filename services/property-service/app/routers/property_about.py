from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.property import Property
from models.property_about import PropertyAbout


router = APIRouter(
    prefix="/property-about",
    tags=["Property About"]
)


# =========================================================
# SCHEMAS
# =========================================================

class PropertyAboutCreate(BaseModel):
    property_id: int
    description: Optional[str] = None
    preferred_tenant: Optional[str] = None
    pets_allowed: bool = False
    smoking_allowed: bool = False
    max_occupancy: Optional[int] = None


class PropertyAboutUpdate(BaseModel):
    property_id: Optional[int] = None
    description: Optional[str] = None
    preferred_tenant: Optional[str] = None
    pets_allowed: Optional[bool] = None
    smoking_allowed: Optional[bool] = None
    max_occupancy: Optional[int] = None


# =========================================================
# CREATE
# =========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_property_about(
    data: PropertyAboutCreate,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Check property exists
    # -----------------------------------------------------

    property_data = (
        db.query(Property)
        .filter(Property.id == data.property_id)
        .first()
    )

    if not property_data:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    # -----------------------------------------------------
    # Because property_id is unique
    # -----------------------------------------------------

    existing = (
        db.query(PropertyAbout)
        .filter(
            PropertyAbout.property_id == data.property_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Property about already exists for this property"
        )

    # -----------------------------------------------------
    # Create
    # -----------------------------------------------------

    property_about = PropertyAbout(
        property_id=data.property_id,
        description=data.description,
        preferred_tenant=data.preferred_tenant,
        pets_allowed=data.pets_allowed,
        smoking_allowed=data.smoking_allowed,
        max_occupancy=data.max_occupancy
    )

    db.add(property_about)
    db.commit()
    db.refresh(property_about)

    return {
        "status": 201,
        "message": "Property about created successfully",
        "data": {
            "id": property_about.id,
            "property_id": property_about.property_id,
            "description": property_about.description,
            "preferred_tenant": property_about.preferred_tenant,
            "pets_allowed": property_about.pets_allowed,
            "smoking_allowed": property_about.smoking_allowed,
            "max_occupancy": property_about.max_occupancy,
            "created_at": property_about.created_at,
            "updated_at": property_about.updated_at
        }
    }


# =========================================================
# GET ALL
# =========================================================

@router.get("")
def get_all_property_about(
    db: Session = Depends(get_db)
):
    property_about_list = (
        db.query(PropertyAbout)
        .order_by(PropertyAbout.id.desc())
        .all()
    )

    if not property_about_list:
        raise HTTPException(
            status_code=404,
            detail="No property about found"
        )

    return {
        "status": 200,
        "message": "Property about fetched successfully",
        "count": len(property_about_list),
        "data": [
            {
                "id": item.id,
                "property_id": item.property_id,
                "description": item.description,
                "preferred_tenant": item.preferred_tenant,
                "pets_allowed": item.pets_allowed,
                "smoking_allowed": item.smoking_allowed,
                "max_occupancy": item.max_occupancy,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
            for item in property_about_list
        ]
    }


# =========================================================
# GET BY ID
# =========================================================

@router.get("/{property_about_id}")
def get_property_about_by_id(
    property_about_id: int,
    db: Session = Depends(get_db)
):
    property_about = (
        db.query(PropertyAbout)
        .filter(
            PropertyAbout.id == property_about_id
        )
        .first()
    )

    if not property_about:
        raise HTTPException(
            status_code=404,
            detail="Property about not found"
        )

    return {
        "status": 200,
        "message": "Property about fetched successfully",
        "data": {
            "id": property_about.id,
            "property_id": property_about.property_id,
            "description": property_about.description,
            "preferred_tenant": property_about.preferred_tenant,
            "pets_allowed": property_about.pets_allowed,
            "smoking_allowed": property_about.smoking_allowed,
            "max_occupancy": property_about.max_occupancy,
            "created_at": property_about.created_at,
            "updated_at": property_about.updated_at
        }
    }


# =========================================================
# GET BY PROPERTY ID
# =========================================================

@router.get("/property/{property_id}")
def get_property_about_by_property_id(
    property_id: int,
    db: Session = Depends(get_db)
):
    property_about = (
        db.query(PropertyAbout)
        .filter(
            PropertyAbout.property_id == property_id
        )
        .first()
    )

    if not property_about:
        raise HTTPException(
            status_code=404,
            detail="Property about not found"
        )

    return {
        "status": 200,
        "message": "Property about fetched successfully",
        "data": {
            "id": property_about.id,
            "property_id": property_about.property_id,
            "description": property_about.description,
            "preferred_tenant": property_about.preferred_tenant,
            "pets_allowed": property_about.pets_allowed,
            "smoking_allowed": property_about.smoking_allowed,
            "max_occupancy": property_about.max_occupancy,
            "created_at": property_about.created_at,
            "updated_at": property_about.updated_at
        }
    }


# =========================================================
# UPDATE
# =========================================================
# All fields are optional.
# Only the fields sent in the request will be updated.
# =========================================================

@router.put("/{property_about_id}")
def update_property_about(
    property_about_id: int,
    data: PropertyAboutUpdate,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Find property about
    # -----------------------------------------------------

    property_about = (
        db.query(PropertyAbout)
        .filter(
            PropertyAbout.id == property_about_id
        )
        .first()
    )

    if not property_about:
        raise HTTPException(
            status_code=404,
            detail="Property about not found"
        )

    # -----------------------------------------------------
    # Update property_id
    # -----------------------------------------------------

    if data.property_id is not None:

        # Check property exists
        property_data = (
            db.query(Property)
            .filter(
                Property.id == data.property_id
            )
            .first()
        )

        if not property_data:
            raise HTTPException(
                status_code=404,
                detail="Property not found"
            )

        # Check another PropertyAbout already uses it
        existing = (
            db.query(PropertyAbout)
            .filter(
                PropertyAbout.property_id == data.property_id,
                PropertyAbout.id != property_about_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Property about already exists for this property"
            )

        property_about.property_id = data.property_id

    # -----------------------------------------------------
    # Update description
    # -----------------------------------------------------

    if data.description is not None:
        property_about.description = data.description

    # -----------------------------------------------------
    # Update preferred tenant
    # -----------------------------------------------------

    if data.preferred_tenant is not None:
        property_about.preferred_tenant = data.preferred_tenant

    # -----------------------------------------------------
    # Update pets allowed
    # -----------------------------------------------------

    if data.pets_allowed is not None:
        property_about.pets_allowed = data.pets_allowed

    # -----------------------------------------------------
    # Update smoking allowed
    # -----------------------------------------------------

    if data.smoking_allowed is not None:
        property_about.smoking_allowed = data.smoking_allowed

    # -----------------------------------------------------
    # Update max occupancy
    # -----------------------------------------------------

    if data.max_occupancy is not None:
        property_about.max_occupancy = data.max_occupancy

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    db.commit()
    db.refresh(property_about)

    return {
        "status": 200,
        "message": "Property about updated successfully",
        "data": {
            "id": property_about.id,
            "property_id": property_about.property_id,
            "description": property_about.description,
            "preferred_tenant": property_about.preferred_tenant,
            "pets_allowed": property_about.pets_allowed,
            "smoking_allowed": property_about.smoking_allowed,
            "max_occupancy": property_about.max_occupancy,
            "created_at": property_about.created_at,
            "updated_at": property_about.updated_at
        }
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/{property_about_id}")
def delete_property_about(
    property_about_id: int,
    db: Session = Depends(get_db)
):
    property_about = (
        db.query(PropertyAbout)
        .filter(
            PropertyAbout.id == property_about_id
        )
        .first()
    )

    if not property_about:
        raise HTTPException(
            status_code=404,
            detail="Property about not found"
        )

    db.delete(property_about)
    db.commit()

    return {
        "status": 200,
        "message": "Property about deleted successfully",
        "data": {
            "id": property_about_id
        }
    }

