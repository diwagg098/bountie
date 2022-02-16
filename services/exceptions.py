from fastapi import HTTPException, status

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

verified_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Please verify your email"
)

duplicate_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Either email, phone or username has been used"
)

otp_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid OTP"
)

inactive_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Account is suspended"
)

admin_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You shall not pass"
)

user_registered_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already registered"
)

invalid_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid Data"
)