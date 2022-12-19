from fastapi import Depends, HTTPException, status

from src.user.schemas import User
# from src.user.security_utils import SECRET_KEY, ALGORITHM, oauth2_scheme, TokenData, jwt, JWTError

from src.database.core import SessionLocal
# from src.user.security_utils import oauth2_scheme
import src.user.userConnector as userConnector


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = userConnector.get_user_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user is None:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
