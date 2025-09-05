# Simple JWT Middleware

## Middleware đơn giản chỉ check JWT token

### Chức năng:
- Kiểm tra JWT token trong Authorization header
- Verify token và lấy username
- Lưu username vào request.state
- Không cần kết nối database để check user

### Cách sử dụng:

#### 1. Middleware tự động check JWT cho tất cả endpoints (trừ excluded paths)

```python
# Các path không cần JWT:
- /
- /health  
- /docs
- /redoc
- /api/users/login
- /api/users/register
```

#### 2. Trong endpoint, lấy username từ request:

```python
from fastapi import Request
from app.middleware.simple_helpers import get_username_from_request

@router.get("/profile")
async def get_profile(request: Request):
    username = get_username_from_request(request)
    return {"username": username}
```

#### 3. Test middleware:

```bash
# Login để lấy token
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"

# Sử dụng token để gọi API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/simple/test-jwt"
```

### Ưu điểm:
- Đơn giản, nhanh
- Chỉ verify JWT, không query database
- Dễ hiểu và maintain
- Phù hợp cho các ứng dụng đơn giản

### So sánh với dependency injection:

**Cách cũ (dependency):**
```python
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
```

**Cách mới (middleware):**
```python  
@router.get("/profile")
async def get_profile(request: Request):
    username = get_username_from_request(request)
    return {"username": username}
```
