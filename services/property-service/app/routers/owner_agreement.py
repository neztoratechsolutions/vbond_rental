import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.owner_agreement import OwnerAgreement


router = APIRouter(
    prefix="/owner-agreements",
    tags=["Owner Agreements"]
)


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = "app/uploads/agreements"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# POST - CREATE AGREEMENT
# =========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_owner_agreement(
    owner_id: int = Form(...),
    agreement_content: str | None = Form(None),
    agreement_pdf: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # At least content or PDF should be provided
    if not agreement_content and not agreement_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agreement content or PDF is required"
        )

    pdf_path = None

    # -----------------------------------------------------
    # Save PDF if provided
    # -----------------------------------------------------

    if agreement_pdf:

        if agreement_pdf.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

        file_extension = ".pdf"

        file_name = f"{uuid.uuid4().hex}{file_extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            file_name
        )

        with open(file_path, "wb") as buffer:
            content = await agreement_pdf.read()
            buffer.write(content)

        pdf_path = file_path

    # -----------------------------------------------------
    # Create database record
    # -----------------------------------------------------

    agreement = OwnerAgreement(
        owner_id=owner_id,
        agreement_content=agreement_content,
        agreement_pdf=pdf_path
    )

    db.add(agreement)
    db.commit()
    db.refresh(agreement)

    return {
        "status": 201,
        "message": "Owner agreement created successfully",
        "data": {
            "id": agreement.id,
            "owner_id": agreement.owner_id,
            "agreement_content": agreement.agreement_content,
            "agreement_pdf": agreement.agreement_pdf,
            "created_at": agreement.created_at,
            "updated_at": agreement.updated_at
        }
    }


# =========================================================
# GET ALL AGREEMENTS
# =========================================================

@router.get("")
def get_all_owner_agreements(
    db: Session = Depends(get_db)
):
    agreements = (
        db.query(OwnerAgreement)
        .order_by(OwnerAgreement.id.desc())
        .all()
    )

    return {
        "status": 200,
        "message": "Owner agreements fetched successfully",
        "count": len(agreements),
        "data": [
            {
                "id": agreement.id,
                "owner_id": agreement.owner_id,
                "agreement_content": agreement.agreement_content,
                "agreement_pdf": agreement.agreement_pdf,
                "created_at": agreement.created_at,
                "updated_at": agreement.updated_at
            }
            for agreement in agreements
        ]
    }


# =========================================================
# GET AGREEMENTS BY OWNER ID
# =========================================================

@router.get("/owner/{owner_id}")
def get_agreements_by_owner(
    owner_id: int,
    db: Session = Depends(get_db)
):
    agreements = (
        db.query(OwnerAgreement)
        .filter(OwnerAgreement.owner_id == owner_id)
        .order_by(OwnerAgreement.id.desc())
        .all()
    )

    if not agreements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No agreement found for this owner"
        )

    return {
        "status": 200,
        "message": "Owner agreements fetched successfully",
        "count": len(agreements),
        "data": [
            {
                "id": agreement.id,
                "owner_id": agreement.owner_id,
                "agreement_content": agreement.agreement_content,
                "agreement_pdf": agreement.agreement_pdf,
                "created_at": agreement.created_at,
                "updated_at": agreement.updated_at
            }
            for agreement in agreements
        ]
    }


# =========================================================
# GET AGREEMENT BY ID
# =========================================================

@router.get("/{agreement_id}")
def get_owner_agreement(
    agreement_id: int,
    db: Session = Depends(get_db)
):
    agreement = (
        db.query(OwnerAgreement)
        .filter(OwnerAgreement.id == agreement_id)
        .first()
    )

    if not agreement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agreement not found"
        )

    return {
        "status": 200,
        "message": "Owner agreement fetched successfully",
        "data": {
            "id": agreement.id,
            "owner_id": agreement.owner_id,
            "agreement_content": agreement.agreement_content,
            "agreement_pdf": agreement.agreement_pdf,
            "created_at": agreement.created_at,
            "updated_at": agreement.updated_at
        }
    }


# =========================================================
# PUT - UPDATE AGREEMENT
# =========================================================

@router.put("/{agreement_id}")
async def update_owner_agreement(
    agreement_id: int,
    owner_id: int | None = Form(None),
    agreement_content: str | None = Form(None),
    agreement_pdf: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    agreement = (
        db.query(OwnerAgreement)
        .filter(OwnerAgreement.id == agreement_id)
        .first()
    )

    if not agreement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agreement not found"
        )

    # -----------------------------------------------------
    # Update owner ID
    # -----------------------------------------------------

    if owner_id is not None:
        agreement.owner_id = owner_id

    # -----------------------------------------------------
    # Update agreement content
    # -----------------------------------------------------

    if agreement_content is not None:
        agreement.agreement_content = agreement_content

    # -----------------------------------------------------
    # Update PDF
    # -----------------------------------------------------

    if agreement_pdf:

        if agreement_pdf.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

        file_name = f"{uuid.uuid4().hex}.pdf"

        file_path = os.path.join(
            UPLOAD_DIR,
            file_name
        )

        with open(file_path, "wb") as buffer:
            content = await agreement_pdf.read()
            buffer.write(content)

        # Delete old PDF if it exists
        if agreement.agreement_pdf:
            if os.path.exists(agreement.agreement_pdf):
                os.remove(agreement.agreement_pdf)

        agreement.agreement_pdf = file_path

    db.commit()
    db.refresh(agreement)

    return {
        "status": 200,
        "message": "Owner agreement updated successfully",
        "data": {
            "id": agreement.id,
            "owner_id": agreement.owner_id,
            "agreement_content": agreement.agreement_content,
            "agreement_pdf": agreement.agreement_pdf,
            "created_at": agreement.created_at,
            "updated_at": agreement.updated_at
        }
    }


# =========================================================
# DELETE AGREEMENT
# =========================================================

@router.delete("/{agreement_id}")
def delete_owner_agreement(
    agreement_id: int,
    db: Session = Depends(get_db)
):
    agreement = (
        db.query(OwnerAgreement)
        .filter(OwnerAgreement.id == agreement_id)
        .first()
    )

    if not agreement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agreement not found"
        )

    # Delete PDF file
    if agreement.agreement_pdf:
        if os.path.exists(agreement.agreement_pdf):
            os.remove(agreement.agreement_pdf)

    db.delete(agreement)
    db.commit()

    return {
        "status": 200,
        "message": "Owner agreement deleted successfully"
    }