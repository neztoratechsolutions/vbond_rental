from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.city import City
from models.state import State

from schemas.city import (
    CityCreate,
    CityUpdate,
    CityResponse
)


router = APIRouter(
    prefix="/api/cities",
    tags=["Cities"]
)


# CREATE CITY
@router.post(
    "",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_city(
    request: CityCreate,
    db: Session = Depends(get_db)
):

    # Check state exists
    state = (
        db.query(State)
        .filter(State.id == request.state_id)
        .first()
    )

    if not state:
        raise HTTPException(
            status_code=404,
            detail="State not found"
        )

    # Check duplicate city in same state
    existing_city = (
        db.query(City)
        .filter(
            City.state_id == request.state_id,
            City.name.ilike(request.name)
        )
        .first()
    )

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City already exists in this state"
        )

    city = City(
        state_id=request.state_id,
        name=request.name,
        is_active=request.is_active
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


# GET ALL CITIES
@router.get(
    "",
    response_model=list[CityResponse]
)
def get_cities(
    db: Session = Depends(get_db)
):

    cities = (
        db.query(City)
        .order_by(City.id.desc())
        .all()
    )

    return cities


# GET SINGLE CITY
@router.get(
    "/{city_id}",
    response_model=CityResponse
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db)
):

    city = (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city


# UPDATE CITY
@router.put(
    "/{city_id}",
    response_model=CityResponse
)
def update_city(
    city_id: int,
    request: CityUpdate,
    db: Session = Depends(get_db)
):

    city = (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    # If state_id is being changed
    if request.state_id is not None:

        state = (
            db.query(State)
            .filter(State.id == request.state_id)
            .first()
        )

        if not state:
            raise HTTPException(
                status_code=404,
                detail="State not found"
            )

        city.state_id = request.state_id

    # Update name
    if request.name is not None:

        existing_city = (
            db.query(City)
            .filter(
                City.state_id == city.state_id,
                City.name.ilike(request.name),
                City.id != city_id
            )
            .first()
        )

        if existing_city:
            raise HTTPException(
                status_code=400,
                detail="City already exists in this state"
            )

        city.name = request.name

    # Update active status
    if request.is_active is not None:
        city.is_active = request.is_active

    db.commit()
    db.refresh(city)

    return city


# DELETE CITY
@router.delete(
    "/{city_id}"
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
):

    city = (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    db.delete(city)
    db.commit()

    return {
        "success": True,
        "message": "City deleted successfully"
    }