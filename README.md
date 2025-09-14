# Đồ án môn học - Web API Python

## Mô tả
Project Web API được xây dựng bằng Python với FastAPI, SQLAlchemy ORM và Alembic migration, theo mô hình MVC.

## Công nghệ sử dụng
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic  
- **Database**: PostgreSQL (Docker)
- **Authentication**: JWT
- **Pattern**: MVC (Model-View-Controller)

## 🚀 Quick Start

### 1. Tạo và kích hoạt virtual environment
```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Khởi động database
```bash
docker-compose up -d
```

### 4. Chạy migration
```bash
# Với virtual environment đã kích hoạt
python -m alembic upgrade head
```

### 5. Khởi động server
```bash
# Với virtual environment đã kích hoạt
python -m uvicorn app.main:app --reload
```

### 6. Truy cập ứng dụng
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Các lệnh thường dùng

**Lưu ý**: Đảm bảo virtual environment đã được kích hoạt trước khi chạy các lệnh Python

### Migration
```bash
# Xem trạng thái migration hiện tại
python -m alembic current

# Xem lịch sử migration
python -m alembic history --verbose

# Tạo migration mới
python -m alembic revision --autogenerate -m "Mô tả thay đổi"

# Chạy migration
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

### Development
```bash
# Khởi động development server
python -m uvicorn app.main:app --reload

# Khởi động với custom host/port
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database
```bash
# Kết nối vào PostgreSQL
docker exec -it postgres-db-doan-python psql -U admin -d myapp

# Xem danh sách tables
docker exec -it postgres-db-doan-python psql -U admin -d myapp -c "\dt"

# Reset database (Cẩn thận - mất hết data!)
docker exec -it postgres-db-doan-python psql -U admin -d myapp -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Docker
```bash
# Khởi động services
docker-compose up -d

# Dừng services
docker-compose down

# Xem logs
docker-compose logs -f

# Restart services
docker-compose restart
```

## 📁 Cấu trúc thư mục
```
doan_python/
├── .venv/                      # Virtual environment
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py         # Database configuration
│   │   └── settings.py         # App settings
│   ├── models/                 # Models (M in MVC)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── brand.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── order_item_inventory.py
│   ├── controllers/            # Controllers (C in MVC)
│   │   ├── __init__.py
│   │   ├── user_controller.py
│   │   └── ...
│   ├── views/                  # Views/Routes (V in MVC)
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   └── ...
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   └── ...
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── auth.py
│       └── helpers.py
├── alembic/                    # Migration files
├── alembic.ini                 # Alembic config
├── docker-compose.yaml         # Docker services
├── requirements.txt
├── .env                        # Environment variables
├── .gitignore
└── MIGRATION_GUIDE.md          # Chi tiết về migration
```

## 🗄️ Database Schema

### Tables được tạo:
- `users` - Quản lý người dùng
- `brands` - Thương hiệu sản phẩm  
- `products` - Sản phẩm
- `inventory` - Kho hàng
- `customers` - Khách hàng
- `orders` - Đơn hàng
- `order_items` - Chi tiết đơn hàng  
- `order_item_inventories` - Liên kết inventory với order items

## 📖 Tài liệu chi tiết

Xem file [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) để biết chi tiết về:
- Cách tạo và quản lý migration
- Troubleshooting
- Best practices
- Các lệnh nâng cao

## 🔧 Cấu hình

### Environment Variables (.env)
```env
DATABASE_URL=postgresql://admin:admin@localhost:5433/myapp
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
```

### Docker Services
- **PostgreSQL**: localhost:5433
- **Container**: postgres-db-doan-python

## 📝 API Endpoints

### Authentication
- `POST /api/users/login` - Đăng nhập
- `POST /api/users/register` - Đăng ký

### Users
- `GET /api/users/me` - Thông tin user hiện tại
- `GET /api/users/` - Danh sách users (có phân trang)
- `GET /api/users/{id}` - Chi tiết user
- `POST /api/users/` - Tạo user mới
- `PUT /api/users/{id}` - Cập nhật user
- `DELETE /api/users/{id}` - Xóa user

## 🚧 Development

### Thêm model mới
1. Tạo file model trong `app/models/`
2. Import model vào `alembic/env.py`
3. Tạo migration: `.\dev.ps1 migration "Add new model"`
4. Chạy migration: `.\dev.ps1 migrate`

### Thêm API endpoint
1. Tạo schema trong `app/schemas/`
2. Tạo controller trong `app/controllers/`
3. Tạo routes trong `app/views/`
4. Import routes vào `app/main.py`

## 📚 Tài liệu tham khảo
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)