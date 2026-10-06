import os
import uuid
from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from database import get_db
from models.property import Property
from models.property_media import PropertyMedia


router = APIRouter(
    prefix="/property-media",
    tags=["Property Media"]
)


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = "app/uploads/property_media"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =========================================================
# ALLOWED FILE TYPES
# =========================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# =========================================================
# CREATE - SINGLE / MULTIPLE IMAGE UPLOAD
# =========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_property_media(
    property_id: Annotated[int, Form(...)],
    media_type: Annotated[str, Form(...)],
    files: Annotated[list[UploadFile], File(...)],
    is_primary: Annotated[bool, Form()] = False,
    display_order: Annotated[int, Form()] = 0,
    db: Session = Depends(get_db),
):

    if not files:
        raise HTTPException(
            status_code=400,
            detail="At least one image is required"
        )

    # -----------------------------------------------------
    # Check property
    # -----------------------------------------------------

    property_data = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_data:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    # -----------------------------------------------------
    # Check existing primary image
    # -----------------------------------------------------

    existing_primary = (
        db.query(PropertyMedia)
        .filter(
            PropertyMedia.property_id == property_id,
            PropertyMedia.is_primary == True
        )
        .first()
    )

    if existing_primary and is_primary:
        raise HTTPException(
            status_code=400,
            detail="Primary image already exists for this property"
        )

    created_media = []

    # -----------------------------------------------------
    # Upload files
    # -----------------------------------------------------

    for index, file in enumerate(files):

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid file name"
            )

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid file type for {file.filename}. "
                    "Only JPG, JPEG, PNG and WEBP images are allowed."
                )
            )

        # -------------------------------------------------
        # Generate unique filename
        # -------------------------------------------------

        unique_filename = (
            f"{uuid.uuid4().hex}{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        file_content = file.file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # -------------------------------------------------
        # First image becomes primary if requested
        # -------------------------------------------------

        current_is_primary = False

        if is_primary and index == 0:
            current_is_primary = True

        file_url = (
            f"/uploads/property_media/{unique_filename}"
        )

        media = PropertyMedia(
            property_id=property_id,
            media_type=media_type,
            file_url=file_url,
            file_name=file.filename,
            is_primary=current_is_primary,
            display_order=display_order + index
        )

        db.add(media)
        db.flush()

        created_media.append(
            {
                "id": media.id,
                "property_id": media.property_id,
                "media_type": media.media_type,
                "file_url": media.file_url,
                "file_name": media.file_name,
                "is_primary": media.is_primary,
                "display_order": media.display_order,
                "created_at": media.created_at
            }
        )

    db.commit()

    return {
        "status": 201,
        "message": "Property media uploaded successfully",
        "count": len(created_media),
        "data": created_media
    }


# =========================================================
# GET ALL
# =========================================================

@router.get("")
def get_all_property_media(
    db: Session = Depends(get_db)
):

    media_list = (
        db.query(PropertyMedia)
        .order_by(PropertyMedia.id.desc())
        .all()
    )

    if not media_list:
        raise HTTPException(
            status_code=404,
            detail="No property media found"
        )

    return {
        "status": 200,
        "message": "Property media fetched successfully",
        "count": len(media_list),
        "data": [
            {
                "id": media.id,
                "property_id": media.property_id,
                "media_type": media.media_type,
                "file_url": media.file_url,
                "file_name": media.file_name,
                "is_primary": media.is_primary,
                "display_order": media.display_order,
                "created_at": media.created_at
            }
            for media in media_list
        ]
    }


# =========================================================
# GET BY PROPERTY ID
# =========================================================

@router.get("/property/{property_id}")
def get_property_media(
    property_id: int,
    db: Session = Depends(get_db)
):

    property_data = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property_data:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    media_list = (
        db.query(PropertyMedia)
        .filter(
            PropertyMedia.property_id == property_id
        )
        .order_by(
            PropertyMedia.display_order.asc(),
            PropertyMedia.id.asc()
        )
        .all()
    )

    if not media_list:
        raise HTTPException(
            status_code=404,
            detail="No media found for this property"
        )

    return {
        "status": 200,
        "message": "Property media fetched successfully",
        "property_id": property_id,
        "count": len(media_list),
        "data": [
            {
                "id": media.id,
                "property_id": media.property_id,
                "media_type": media.media_type,
                "file_url": media.file_url,
                "file_name": media.file_name,
                "is_primary": media.is_primary,
                "display_order": media.display_order,
                "created_at": media.created_at
            }
            for media in media_list
        ]
    }


# =========================================================
# GET BY MEDIA ID
# =========================================================

@router.get("/{media_id}")
def get_property_media_by_id(
    media_id: int,
    db: Session = Depends(get_db)
):

    media = (
        db.query(PropertyMedia)
        .filter(PropertyMedia.id == media_id)
        .first()
    )

    if not media:
        raise HTTPException(
            status_code=404,
            detail="Property media not found"
        )

    return {
        "status": 200,
        "message": "Property media fetched successfully",
        "data": {
            "id": media.id,
            "property_id": media.property_id,
            "media_type": media.media_type,
            "file_url": media.file_url,
            "file_name": media.file_name,
            "is_primary": media.is_primary,
            "display_order": media.display_order,
            "created_at": media.created_at
        }
    }


# =========================================================
# UPDATE
# =========================================================

@router.put("/{media_id}")
def update_property_media(
    media_id: int,

    property_id: Annotated[
        Optional[int],
        Form()
    ] = None,

    media_type: Annotated[
        Optional[str],
        Form()
    ] = None,

    file: Annotated[
        Optional[UploadFile],
        File()
    ] = None,

    is_primary: Annotated[
        Optional[bool],
        Form()
    ] = None,

    display_order: Annotated[
        Optional[int],
        Form()
    ] = None,

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find media
    # -----------------------------------------------------

    media = (
        db.query(PropertyMedia)
        .filter(PropertyMedia.id == media_id)
        .first()
    )

    if not media:
        raise HTTPException(
            status_code=404,
            detail="Property media not found"
        )

    # -----------------------------------------------------
    # Update property_id
    # -----------------------------------------------------

    if property_id is not None:

        property_data = (
            db.query(Property)
            .filter(Property.id == property_id)
            .first()
        )

        if not property_data:
            raise HTTPException(
                status_code=404,
                detail="Property not found"
            )

        media.property_id = property_id

    # -----------------------------------------------------
    # Update media_type
    # -----------------------------------------------------

    if media_type is not None:

        media.media_type = media_type

    # -----------------------------------------------------
    # Update is_primary
    # -----------------------------------------------------

    if is_primary is not None:

        if is_primary is True:

            existing_primary = (
                db.query(PropertyMedia)
                .filter(
                    PropertyMedia.property_id == media.property_id,
                    PropertyMedia.is_primary == True,
                    PropertyMedia.id != media_id
                )
                .first()
            )

            if existing_primary:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Primary image already exists "
                        "for this property"
                    )
                )

        media.is_primary = is_primary

    # -----------------------------------------------------
    # Update display_order
    # -----------------------------------------------------

    if display_order is not None:

        media.display_order = display_order

    # -----------------------------------------------------
    # Update image file
    # -----------------------------------------------------

    if file is not None:

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid file name"
            )

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, JPEG, PNG and WEBP "
                    "images are allowed."
                )
            )

        # ---------------------------------------------
        # Delete old physical file
        # ---------------------------------------------

        if media.file_url:

            old_file_name = os.path.basename(
                media.file_url
            )

            old_file_path = os.path.join(
                UPLOAD_DIR,
                old_file_name
            )

            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # ---------------------------------------------
        # Save new file
        # ---------------------------------------------

        unique_filename = (
            f"{uuid.uuid4().hex}{extension}"
        )

        new_file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        file_content = file.file.read()

        with open(new_file_path, "wb") as buffer:
            buffer.write(file_content)

        media.file_url = (
            f"/uploads/property_media/{unique_filename}"
        )

        media.file_name = file.filename

    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    db.commit()
    db.refresh(media)

    return {
        "status": 200,
        "message": "Property media updated successfully",
        "data": {
            "id": media.id,
            "property_id": media.property_id,
            "media_type": media.media_type,
            "file_url": media.file_url,
            "file_name": media.file_name,
            "is_primary": media.is_primary,
            "display_order": media.display_order,
            "created_at": media.created_at
        }
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/{media_id}")
def delete_property_media(
    media_id: int,
    db: Session = Depends(get_db)
):

    media = (
        db.query(PropertyMedia)
        .filter(PropertyMedia.id == media_id)
        .first()
    )

    if not media:
        raise HTTPException(
            status_code=404,
            detail="Property media not found"
        )

    # -----------------------------------------------------
    # Delete physical file
    # -----------------------------------------------------

    if media.file_url:

        file_name = os.path.basename(
            media.file_url
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            file_name
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    # -----------------------------------------------------
    # Delete database record
    # -----------------------------------------------------

    db.delete(media)
    db.commit()

    return {
        "status": 200,
        "message": "Property media deleted successfully",
        "data": {
            "id": media_id
        }
    }

