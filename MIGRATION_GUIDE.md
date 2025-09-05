# Hướng dẫn Migration và Run Project

## 📋 Mục lục
1. [Cài đặt và Khởi tạo](#cài-đặt-và-khởi-tạo)
2. [Quản lý Database Migration](#quản-lý-database-migration)
3. [Chạy Project](#chạy-project)
4. [Các lệnh thường dùng](#các-lệnh-thường-dùng)
5. [Troubleshooting](#troubleshooting)

## 🚀 Cài đặt và Khởi tạo

### 1. Clone project và cài đặt dependencies
```bash
# Clone project
git clone <repository-url>
cd doan_python

# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD  
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate

# Cài đặt packages (với virtual environment đã kích hoạt)
pip install -r requirements.txt
```

### 2. Cấu hình môi trường
```bash
# Copy file .env.example thành .env (nếu có)
# Hoặc cập nhật file .env với thông tin database của bạn
```

Nội dung file `.env`:
```env
# Database
DATABASE_URL=postgresql://admin:admin@localhost:5433/myapp

# App Settings
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Environment
ENVIRONMENT=development
```

### 3. Khởi động Database (PostgreSQL với Docker)
```bash
# Khởi động PostgreSQL container
docker-compose up -d

# Kiểm tra container đang chạy
docker ps

# Kiểm tra logs nếu cần
docker-compose logs postgres
```

## 🗄️ Quản lý Database Migration

### Khái niệm Migration
Migration là cách quản lý thay đổi cấu trúc database theo thời gian. Mỗi migration file chứa các thay đổi cần áp dụng lên database.

### Các lệnh Migration cơ bản

#### 1. Kiểm tra trạng thái migration hiện tại
```bash
# Xem migration nào đã được áp dụng
python -m alembic current

# Xem lịch sử migration
python -m alembic history --verbose
```

#### 2. Tạo migration mới

**Tự động tạo migration từ thay đổi model:**
```bash
# Alembic sẽ so sánh model hiện tại với database và tạo migration
python -m alembic revision --autogenerate -m "Mô tả thay đổi"

# Ví dụ:
python -m alembic revision --autogenerate -m "Add email field to users table"
python -m alembic revision --autogenerate -m "Create products table"
```

**Tạo migration trống (để viết thủ công):**
```bash
python -m alembic revision -m "Mô tả thay đổi"
```

#### 3. Áp dụng migration

```bash
# Áp dụng tất cả migration chưa chạy
python -m alembic upgrade head

# Áp dụng đến một revision cụ thể
python -m alembic upgrade <revision_id>

# Ví dụ:
python -m alembic upgrade ae1027a6acf
```

#### 4. Rollback migration

```bash
# Rollback về migration trước đó
python -m alembic downgrade -1

# Rollback về một revision cụ thể
python -m alembic downgrade <revision_id>

# Rollback tất cả
python -m alembic downgrade base
```

### Quy trình tạo migration khi thay đổi model

1. **Chỉnh sửa model trong `app/models/`**
   ```python
   # Ví dụ: Thêm field mới vào User model
   class User(Base):
       __tablename__ = "users"
       
       id = Column(Integer, primary_key=True)
       username = Column(String(50), unique=True, nullable=False)
       email = Column(String(100), nullable=True)  # Field mới
       # ... các field khác
   ```

2. **Import model mới vào `alembic/env.py`** (nếu là model mới)
   ```python
   from app.models.user import User
   from app.models.new_model import NewModel  # Model mới
   ```

3. **Tạo migration**
   ```bash
   python -m alembic revision --autogenerate -m "Add email to users table"
   ```

4. **Kiểm tra migration file được tạo**
   - File sẽ được tạo trong `alembic/versions/`
   - Xem lại nội dung để đảm bảo đúng

5. **Áp dụng migration**
   ```bash
   python -m alembic upgrade head
   ```

6. **Kiểm tra database**
   ```bash
   # Kết nối vào database để kiểm tra
   docker exec -it postgres-db-doan-python psql -U admin -d myapp
   \dt  # Liệt kê tables
   \d users  # Xem cấu trúc bảng users
   ```

## 🏃 Chạy Project

### 1. Development Mode
```bash
# Chạy với auto-reload (development)
python -m uvicorn app.main:app --reload

# Hoặc chỉ định host và port
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Production Mode
```bash
# Chạy production (không có reload)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Truy cập ứng dụng
- **API Root**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Các lệnh thường dùng

### Database
```bash
# Xóa tất cả data và tạo lại schema
docker exec -it postgres-db-doan-python psql -U admin -d myapp -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Backup database
docker exec postgres-db-doan-python pg_dump -U admin myapp > backup.sql

# Restore database
docker exec -i postgres-db-doan-python psql -U admin myapp < backup.sql

# Kết nối vào database
docker exec -it postgres-db-doan-python psql -U admin -d myapp
```

### Docker
```bash
# Khởi động services
docker-compose up -d

# Dừng services
docker-compose down

# Xem logs
docker-compose logs -f

# Rebuild images
docker-compose up -d --build
```

### Development
```bash
# Kiểm tra syntax errors
python -m py_compile app/main.py

# Format code (nếu có black)
black app/

# Lint code (nếu có flake8)
flake8 app/
```

## 🔧 Troubleshooting

### Lỗi thường gặp và cách khắc phục

#### 1. Migration conflicts
```bash
# Lỗi: "Multiple heads"
python -m alembic heads

# Merge multiple heads
python -m alembic merge -m "Merge heads" head1 head2
```

#### 2. Database connection error
```bash
# Kiểm tra database có chạy không
docker ps | grep postgres

# Kiểm tra port
netstat -an | findstr 5433
```

#### 3. Migration không detect thay đổi
- Đảm bảo model được import trong `alembic/env.py`
- Kiểm tra `target_metadata = Base.metadata`
- Xóa `__pycache__` và thử lại

#### 4. Port đã được sử dụng
```bash
# Thay đổi port trong docker-compose.yaml
ports:
  - "5434:5432"  # Thay vì 5433:5432

# Cập nhật DATABASE_URL trong .env
DATABASE_URL=postgresql://admin:admin@localhost:5434/myapp
```

### Reset hoàn toàn database
```bash
# 1. Dừng container
docker-compose down

# 2. Xóa volume
docker volume rm doan_python_postgres_data_python

# 3. Khởi động lại
docker-compose up -d

# 4. Chạy migration
python -m alembic upgrade head
```

## 📝 Best Practices

1. **Luôn backup database trước khi chạy migration production**
2. **Kiểm tra migration file trước khi apply**
3. **Sử dụng meaningful messages cho migration**
4. **Test migration trên môi trường development trước**
5. **Không chỉnh sửa migration đã apply**
6. **Commit migration files cùng với code changes**

## 🔗 Tài liệu tham khảo
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
