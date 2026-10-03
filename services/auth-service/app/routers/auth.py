from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
import random
from datetime import datetime, timedelta, timezone
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    UpdateProfileRequest,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest
)
from app.core.mail import send_otp_email
from app.models.otp import OTPVerification

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# =========================================================
# AUTHENTICATION
# =========================================================

security = HTTPBearer()


# =========================================================
# GET CURRENT LOGGED-IN USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        # Decode JWT token
        payload = decode_access_token(token)

        # Get user ID from token
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

        # Convert user ID to integer
        try:
            user_id = int(user_id)

        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )

        # Find user in database
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check active status
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Validate user type
    # -----------------------------------------------------

    if request.user_type not in [
        "owner",
        "tenant",
        "technician"
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user type"
        )

    # -----------------------------------------------------
    # Check email already exists
    # -----------------------------------------------------

    existing_email = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # -----------------------------------------------------
    # Check phone already exists
    # -----------------------------------------------------

    existing_phone = (
        db.query(User)
        .filter(User.phone == request.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered"
        )

    # -----------------------------------------------------
    # Create user
    # -----------------------------------------------------

    user = User(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password_hash=hash_password(request.password),
        user_type=request.user_type
    )

    # -----------------------------------------------------
    # Save user
    # -----------------------------------------------------

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find user by email
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # -----------------------------------------------------
    # Verify password
    # -----------------------------------------------------

    if not verify_password(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # -----------------------------------------------------
    # Check active status
    # -----------------------------------------------------

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # -----------------------------------------------------
    # Create access token
    # -----------------------------------------------------

    access_token = create_access_token(
        user.id,
        user.user_type
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# GET LOGGED-IN USER
# =========================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


# =========================================================
# UPDATE LOGGED-IN USER PROFILE
# =========================================================

@router.put(
    "/me",
    response_model=UserResponse
)
def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Update full name
    # -----------------------------------------------------

    if request.full_name is not None:

        current_user.full_name = request.full_name

    # -----------------------------------------------------
    # Update email
    # -----------------------------------------------------

    if request.email is not None:

        existing_email = (
            db.query(User)
            .filter(
                User.email == request.email,
                User.id != current_user.id
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        current_user.email = request.email

    # -----------------------------------------------------
    # Update phone
    # -----------------------------------------------------

    if request.phone is not None:

        existing_phone = (
            db.query(User)
            .filter(
                User.phone == request.phone,
                User.id != current_user.id
            )
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already registered"
            )

        current_user.phone = request.phone

    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    db.commit()
    db.refresh(current_user)

    return current_user




@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found"
        )

    otp = str(
        random.randint(100000, 999999)
    )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=5)
    )

    otp_record = OTPVerification(
        user_id=user.id,
        email=user.email,
        otp=otp,
        expires_at=expires_at,
        is_verified=False
    )

    db.add(otp_record)
    db.commit()

    send_otp_email(
        user.email,
        otp
    )

    return {
        "message": "OTP sent successfully"
    }



@router.post(
    "/verify-otp",
    status_code=status.HTTP_200_OK
)
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp_record = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.user_id == user.id,
            OTPVerification.otp == request.otp,
            OTPVerification.is_verified == False
        )
        .order_by(
            OTPVerification.created_at.desc()
        )
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    now = datetime.now(timezone.utc)

    if now > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
        )

    otp_record.is_verified = True

    db.commit()

    return {
        "message": "OTP verified successfully"
    }



@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK
)
def change_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp_record = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.user_id == user.id,
            OTPVerification.is_verified == True
        )
        .order_by(
            OTPVerification.created_at.desc()
        )
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify OTP first"
        )

    user.password_hash = hash_password(
        request.new_password
    )

    db.delete(otp_record)

    db.commit()

    return {
        "message": "Password changed successfully"
    }



@router.post(
    "/logout",
    status_code=status.HTTP_200_OK
)
def logout(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Logout successful"
    }