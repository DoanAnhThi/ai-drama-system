# Chọn Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /code

# Cài đặt các dependencies hệ thống
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Sao chép các tệp yêu cầu vào container
COPY requirements.txt .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của ứng dụng vào container
COPY . .

# Mở cổng mà ứng dụng sẽ chạy
EXPOSE 8000

# Chạy FastAPI với Uvicorn khi container khởi động
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
