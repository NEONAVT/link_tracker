from fastapi import HTTPException
from fastapi import status

class InvalidTimeRangeError(HTTPException):
    def __init__(self):
        logger.warning("Invalid time range provided")
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter 'from' must be less than or equal to 'to'"
        )

class DomainValidationError(HTTPException):
    def __init__(self, invalid_url: str):
        logger.warning(f"Invalid URL format: {invalid_url}")
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid URL format: {invalid_url}"
        )

class RedisConnectionError(HTTPException):
    def __init__(self):
        logger.error("Redis connection failed")
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to Redis database"
        )