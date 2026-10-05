from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.state import State
from schemas.state import (
    StateCreate,
    StateUpdate,
    StateResponse
)


router = APIRouter(
    prefix="/api/states",
    tags=["States"]
)


# CREATE STATE
@router.post(
    "",
    response_model=StateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_state(
    request: StateCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate state name
    existing_state = (
        db.query(State)
        .filter(State.name.ilike(request.name))
        .first()
    )

    if existing_state:
        raise HTTPException(
            status_code=400,
            detail="State already exists"
        )

    # Check duplicate code
    if request.code:

        existing_code = (
            db.query(State)
            .filter(State.code.ilike(request.code))
            .first()
        )

        if existing_code:
            raise HTTPException(
                status_code=400,
                detail="State code already exists"
            )

    state = State(
        name=request.name,
        code=request.code,
        is_active=request.is_active
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


# GET ALL STATES
@router.get(
    "",
    response_model=list[StateResponse]
)
def get_states(
    db: Session = Depends(get_db)
):

    states = (
        db.query(State)
        .order_by(State.id.desc())
        .all()
    )

    return states


# GET SINGLE STATE
@router.get(
    "/{state_id}",
    response_model=StateResponse
)
def get_state(
    state_id: int,
    db: Session = Depends(get_db)
):

    state = (
        db.query(State)
        .filter(State.id == state_id)
        .first()
    )

    if not state:
        raise HTTPException(
            status_code=404,
            detail="State not found"
        )

    return state


# UPDATE STATE
@router.put(
    "/{state_id}",
    response_model=StateResponse
)
def update_state(
    state_id: int,
    request: StateUpdate,
    db: Session = Depends(get_db)
):

    state = (
        db.query(State)
        .filter(State.id == state_id)
        .first()
    )

    if not state:
        raise HTTPException(
            status_code=404,
            detail="State not found"
        )

    # Update name
    if request.name is not None:

        existing_state = (
            db.query(State)
            .filter(
                State.name.ilike(request.name),
                State.id != state_id
            )
            .first()
        )

        if existing_state:
            raise HTTPException(
                status_code=400,
                detail="State name already exists"
            )

        state.name = request.name

    # Update code
    if request.code is not None:

        existing_code = (
            db.query(State)
            .filter(
                State.code.ilike(request.code),
                State.id != state_id
            )
            .first()
        )

        if existing_code:
            raise HTTPException(
                status_code=400,
                detail="State code already exists"
            )

        state.code = request.code

    # Update active status
    if request.is_active is not None:
        state.is_active = request.is_active

    db.commit()
    db.refresh(state)

    return state


# DELETE STATE - SOFT DELETE
@router.delete(
    "/{state_id}"
)
def delete_state(
    state_id: int,
    db: Session = Depends(get_db)
):

    state = (
        db.query(State)
        .filter(State.id == state_id)
        .first()
    )

    if not state:
        raise HTTPException(
            status_code=404,
            detail="State not found"
        )

    state.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "State deleted successfully"
    }