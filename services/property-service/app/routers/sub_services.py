from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.sub_service import SubService
from models.service import Service

from schemas.service import (
    SubServiceCreate,
    SubServiceUpdate,
    SubServiceResponse
)


router = APIRouter(
    prefix="/api/sub-services",
    tags=["Sub Services"]
)


# CREATE
@router.post(
    "",
    response_model=SubServiceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_sub_service(
    request: SubServiceCreate,
    db: Session = Depends(get_db)
):
    # Check service exists
    service = (
        db.query(Service)
        .filter(
            Service.id == request.service_id,
            Service.is_active == True
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # Check duplicate sub-service under same service
    existing_sub_service = (
        db.query(SubService)
        .filter(
            SubService.service_id == request.service_id,
            SubService.name.ilike(request.name)
        )
        .first()
    )

    if existing_sub_service:
        raise HTTPException(
            status_code=400,
            detail="Sub service already exists under this service"
        )

    sub_service = SubService(
        service_id=request.service_id,
        name=request.name,
        description=request.description,
        is_active=request.is_active
    )

    db.add(sub_service)
    db.commit()
    db.refresh(sub_service)

    return sub_service


# GET ALL
@router.get(
    "",
    response_model=list[SubServiceResponse]
)
def get_sub_services(
    db: Session = Depends(get_db)
):
    sub_services = (
        db.query(SubService)
        .order_by(SubService.id.desc())
        .all()
    )

    return sub_services


# GET ONE
@router.get(
    "/{sub_service_id}",
    response_model=SubServiceResponse
)
def get_sub_service(
    sub_service_id: int,
    db: Session = Depends(get_db)
):
    sub_service = (
        db.query(SubService)
        .filter(SubService.id == sub_service_id)
        .first()
    )

    if not sub_service:
        raise HTTPException(
            status_code=404,
            detail="Sub service not found"
        )

    return sub_service


# UPDATE
@router.put(
    "/{sub_service_id}",
    response_model=SubServiceResponse
)
def update_sub_service(
    sub_service_id: int,
    request: SubServiceUpdate,
    db: Session = Depends(get_db)
):
    sub_service = (
        db.query(SubService)
        .filter(SubService.id == sub_service_id)
        .first()
    )

    if not sub_service:
        raise HTTPException(
            status_code=404,
            detail="Sub service not found"
        )

    # Determine service_id after update
    new_service_id = (
        request.service_id
        if request.service_id is not None
        else sub_service.service_id
    )

    # Check service exists
    service = (
        db.query(Service)
        .filter(
            Service.id == new_service_id,
            Service.is_active == True
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # Check duplicate name
    if request.name is not None:
        existing_sub_service = (
            db.query(SubService)
            .filter(
                SubService.service_id == new_service_id,
                SubService.name.ilike(request.name),
                SubService.id != sub_service_id
            )
            .first()
        )

        if existing_sub_service:
            raise HTTPException(
                status_code=400,
                detail="Sub service name already exists under this service"
            )

        sub_service.name = request.name

    if request.service_id is not None:
        sub_service.service_id = request.service_id

    if request.description is not None:
        sub_service.description = request.description

    if request.is_active is not None:
        sub_service.is_active = request.is_active

    db.commit()
    db.refresh(sub_service)

    return sub_service


# DELETE - SOFT DELETE
@router.delete(
    "/{sub_service_id}"
)
def delete_sub_service(
    sub_service_id: int,
    db: Session = Depends(get_db)
):
    sub_service = (
        db.query(SubService)
        .filter(SubService.id == sub_service_id)
        .first()
    )

    if not sub_service:
        raise HTTPException(
            status_code=404,
            detail="Sub service not found"
        )

    sub_service.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "Sub service deleted successfully"
    }