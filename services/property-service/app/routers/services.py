import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session

from database import get_db
from models.service import Service

from schemas.service import ServiceResponse


router = APIRouter(
    prefix="/api/services",
    tags=["Services"]
)


# Upload folder
UPLOAD_DIR = "uploads/services"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# Allowed image formats
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# --------------------------------------------------
# CREATE SERVICE
# --------------------------------------------------

@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_service(
    name: str = Form(...),
    description: str | None = Form(None),
    is_active: bool = Form(True),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    # Check duplicate service name
    existing_service = (
        db.query(Service)
        .filter(Service.name.ilike(name))
        .first()
    )

    if existing_service:
        raise HTTPException(
            status_code=400,
            detail="Service already exists"
        )

    image_url = None

    # Upload image
    if image:

        extension = os.path.splitext(
            image.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG, PNG and WEBP images are allowed"
            )

        filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(
                image.file.read()
            )

        image_url = f"/uploads/services/{filename}"

    # Create service
    service = Service(
        name=name,
        description=description,
        image_url=image_url,
        is_active=is_active
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


# --------------------------------------------------
# GET ALL SERVICES
# --------------------------------------------------

@router.get(
    "",
    response_model=list[ServiceResponse]
)
def get_services(
    db: Session = Depends(get_db)
):

    services = (
        db.query(Service)
        .order_by(Service.id.desc())
        .all()
    )

    return services


# --------------------------------------------------
# GET SINGLE SERVICE
# --------------------------------------------------

@router.get(
    "/{service_id}",
    response_model=ServiceResponse
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service


# --------------------------------------------------
# UPDATE SERVICE
# --------------------------------------------------

@router.put(
    "/{service_id}",
    response_model=ServiceResponse
)
def update_service(
    service_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    is_active: bool | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    # Find service
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # ----------------------------------------------
    # Update name
    # ----------------------------------------------

    if name is not None:

        existing_service = (
            db.query(Service)
            .filter(
                Service.name.ilike(name),
                Service.id != service_id
            )
            .first()
        )

        if existing_service:
            raise HTTPException(
                status_code=400,
                detail="Service name already exists"
            )

        service.name = name

    # ----------------------------------------------
    # Update description
    # ----------------------------------------------

    if description is not None:
        service.description = description

    # ----------------------------------------------
    # Update active status
    # ----------------------------------------------

    if is_active is not None:
        service.is_active = is_active

    # ----------------------------------------------
    # Update image
    # ----------------------------------------------

    if image:

        extension = os.path.splitext(
            image.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG, PNG and WEBP images are allowed"
            )

        filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(
                image.file.read()
            )

        service.image_url = f"/uploads/services/{filename}"

    db.commit()
    db.refresh(service)

    return service


# --------------------------------------------------
# DELETE SERVICE - SOFT DELETE
# --------------------------------------------------

@router.delete(
    "/{service_id}"
)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    service.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "Service deleted successfully"
    }

