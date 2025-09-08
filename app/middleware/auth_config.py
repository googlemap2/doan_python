EXCLUDED_PATHS = {
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
}

EXCLUDED_PATHS_WITH_METHODS = {
    "/user/login": ["POST"],
    "/user": ["POST"],
    "/user/": ["POST"],
}

ENABLE_AUTH_MIDDLEWARE = True

LOG_AUTH_REQUESTS = True

USER_CACHE_TTL = 300

ERROR_MESSAGES = {
    "missing_auth_header": "Authorization header required",
    "invalid_auth_format": "Invalid authorization format. Use 'Bearer <token>'",
    "invalid_token": "Invalid or expired token",
    "user_not_found": "User associated with token does not exist",
    "inactive_user": "User account is inactive",
    "insufficient_permissions": "Insufficient permissions",
    "internal_error": "An error occurred during authentication",
}
