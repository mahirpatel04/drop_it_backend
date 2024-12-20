from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext

from app.core import logger
from app.schemas import CreateUserRequest


def create_user(create_user_request: CreateUserRequest, bcrypt_context: CryptContext, db: Session):
    # Check for duplicate username or email
    existing_user = db.query(User).filter((User.username == create_user_request.username) | (User.email == create_user_request.email)).first()

    if existing_user:
        logger.info(f"Username: \"{existing_user.username}\" and email: \"{existing_user.email}\" already exists")
        raise ValueError("Username or email already exists.")

    # Create a new user
    user = User(
        first_name=create_user_request.first_name,
        birthdate=create_user_request.birthdate,
        username=create_user_request.username,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
        private=create_user_request.private
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # Fetch the latest user data after the commit
    return user
