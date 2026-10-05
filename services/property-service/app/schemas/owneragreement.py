from typing import Optional

from pydantic import BaseModel


class OwnerAgreementResponse(BaseModel):
    id: int
    owner_id: int
    agreement_content: Optional[str] = None
    agreement_pdf: Optional[str] = None

    class Config:
        from_attributes = True