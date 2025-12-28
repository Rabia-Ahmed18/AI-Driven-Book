import time
from collections import defaultdict
from fastapi import Request, HTTPException
from ..core.config import settings
from ..core.logging import app_logger


# Simple in-memory rate limiter (for demo purposes)
# In production, use Redis or similar for distributed rate limiting
request_counts = defaultdict(list)


async def rate_limit_middleware(request: Request, call_next):
    # Get client IP
    client_ip = request.client.host

    # Current time
    current_time = time.time()

    # Clean old requests (older than the window)
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if current_time - req_time < settings.RATE_LIMIT_WINDOW
    ]

    # Check if request count exceeds limit
    if len(request_counts[client_ip]) >= settings.RATE_LIMIT_REQUESTS:
        app_logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Add current request
    request_counts[client_ip].append(current_time)

    response = await call_next(request)
    return response