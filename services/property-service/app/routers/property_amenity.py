from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.property_amenity import PropertyAmenity


router = APIRouter(
    prefix="/property-amenities",
    tags=["Property Amenities"]
)


# =========================================================
# SCHEMA
# =========================================================

class PropertyAmenityCreate(BaseModel):
    property_id: int
    amenity_id: int


class PropertyAmenityUpdate(BaseModel):
    property_id: int
    amenity_id: int


# =========================================================
# CREATE
# =========================================================

@router.post("", status_code=status.HTTP_201_CREATED)
def create_property_amenity(
    data: PropertyAmenityCreate,
    db: Session = Depends(get_db)
):
    property_amenity = PropertyAmenity(
        property_id=data.property_id,
        amenity_id=data.amenity_id
    )

    db.add(property_amenity)
    db.commit()
    db.refresh(property_amenity)

    return {
        "status": 201,
        "message": "Property amenity created successfully",
        "data": {
            "id": property_amenity.id,
            "property_id": property_amenity.property_id,
            "amenity_id": property_amenity.amenity_id
        }
    }


# =========================================================
# GET ALL
# =========================================================

@router.get("")
def get_all_property_amenities(
    db: Session = Depends(get_db)
):
    property_amenities = (
        db.query(PropertyAmenity)
        .order_by(PropertyAmenity.id.desc())
        .all()
    )

    return {
        "status": 200,
        "message": "Property amenities fetched successfully",
        "count": len(property_amenities),
        "data": [
            {
                "id": item.id,
                "property_id": item.property_id,
                "amenity_id": item.amenity_id
            }
            for item in property_amenities
        ]
    }


# =========================================================
# GET BY ID
# =========================================================

@router.get("/{property_amenity_id}")
def get_property_amenity(
    property_amenity_id: int,
    db: Session = Depends(get_db)
):
    property_amenity = (
        db.query(PropertyAmenity)
        .filter(PropertyAmenity.id == property_amenity_id)
        .first()
    )

    if not property_amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property amenity not found"
        )

    return {
        "status": 200,
        "message": "Property amenity fetched successfully",
        "data": {
            "id": property_amenity.id,
            "property_id": property_amenity.property_id,
            "amenity_id": property_amenity.amenity_id
        }
    }


# =========================================================
# GET BY PROPERTY ID
# =========================================================

@router.get("/property/{property_id}")
def get_amenities_by_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property_amenities = (
        db.query(PropertyAmenity)
        .filter(PropertyAmenity.property_id == property_id)
        .order_by(PropertyAmenity.id.desc())
        .all()
    )

    if not property_amenities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No amenities found for this property"
        )

    return {
        "status": 200,
        "message": "Property amenities fetched successfully",
        "count": len(property_amenities),
        "data": [
            {
                "id": item.id,
                "property_id": item.property_id,
                "amenity_id": item.amenity_id
            }
            for item in property_amenities
        ]
    }


# =========================================================
# UPDATE
# =========================================================

@router.put("/{property_amenity_id}")
def update_property_amenity(
    property_amenity_id: int,
    data: PropertyAmenityUpdate,
    db: Session = Depends(get_db)
):
    property_amenity = (
        db.query(PropertyAmenity)
        .filter(PropertyAmenity.id == property_amenity_id)
        .first()
    )

    if not property_amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property amenity not found"
        )

    property_amenity.property_id = data.property_id
    property_amenity.amenity_id = data.amenity_id

    db.commit()
    db.refresh(property_amenity)

    return {
        "status": 200,
        "message": "Property amenity updated successfully",
        "data": {
            "id": property_amenity.id,
            "property_id": property_amenity.property_id,
            "amenity_id": property_amenity.amenity_id
        }
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/{property_amenity_id}")
def delete_property_amenity(
    property_amenity_id: int,
    db: Session = Depends(get_db)
):
    property_amenity = (
        db.query(PropertyAmenity)
        .filter(PropertyAmenity.id == property_amenity_id)
        .first()
    )

    if not property_amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property amenity not found"
        )

    db.delete(property_amenity)
    db.commit()

    return {
        "status": 200,
        "message": "Property amenity deleted successfully"
    }