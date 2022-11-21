from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from carnage.constants import JWT_ALGORITHM, JWT_SECRET_KEY


def generate_jwt(claims: dict[str, Any]) -> str:
    if "aud" in claims:
        claims.pop("aud")

    if "at_hash" in claims:
        claims.pop("at_hash")

    # Replace or append whatever iat/exp that the claims have
    iat = datetime.utcnow()
    exp = iat + timedelta(hours=1)
    claims["iat"] = int(iat.timestamp())
    claims["exp"] = int(exp.timestamp())

    token = jwt.encode(
        claims=claims,
        key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token


def validate_jwt(token: str) -> bool:
    try:
        decoded_token = jwt.decode(
            token=token,
            key=JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        utcnow = int(datetime.utcnow().timestamp())
        is_token_valid = decoded_token["exp"] >= utcnow
        return is_token_valid
    except ExpiredSignatureError:
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> bool:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request,
        )
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code.",
            )

    def verify_jwt(self, token: str) -> bool:
        return validate_jwt(token=token)