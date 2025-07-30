
FROM python:3.11-slim

# 安裝系統依賴（包含 PostGIS 必要套件）
RUN apt-get update && apt-get install -y \
    binutils \
    gdal-bin \
    libgdal-dev \
    postgis \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 設定環境變數，讓 GDAL 正確被找到
ENV GDAL_VERSION=3.4.1
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV PATH="/usr/local/bin:$PATH"

# 建立並切換工作目錄
WORKDIR /app

# 複製 Python 需求檔案並安裝
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 複製專案程式碼
COPY . .

# 對外開放 8000 port (Django 預設 port)
EXPOSE 8000

# 啟動 Django 項目 (可視專案需求調整)
CMD ["gunicorn", "CalgaryCommunity.wsgi:application", "--bind", "0.0.0.0:8000"]