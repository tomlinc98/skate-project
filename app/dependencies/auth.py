from fastapi import Depends, HTTPException, status
from app.core.auth import decode_access_token
from app.services.user import get_user_by_id
from app.models.user import User
from sqlalchemy.orm import Session
from app.dependencies.db import get_db_session


def get_current_user(token: str, db: Session = Depends(get_db_session)) -> User:
    """Retrieve the current user based on the provided token."""
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
