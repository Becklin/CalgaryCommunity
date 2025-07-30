# 使用 Ubuntu 為基底
FROM ubuntu:22.04

# 環境設定避免 tzdata 等互動式安裝
ENV DEBIAN_FRONTEND=noninteractive

# 安裝系統與空間分析相關套件
RUN apt-get update && \
    apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    build-essential \
    binutils \
    libproj-dev \
    libgdal-dev \
    gdal-bin \
    libgeos-dev \
    libpq-dev \
    curl && \
    apt-get clean

# Python alias（確保使用的是 python3.11）
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# 設定 GDAL 環境變數（GeoDjango 需要）
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# 設定專案目錄
WORKDIR /app

# 複製專案到容器中
COPY . .

# 安裝 Python 套件
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 對外開放埠號
EXPOSE 8000

# 啟動指令（使用 gunicorn）
CMD ["sh", "-c", "python manage.py migrate && gunicorn calCrimes.wsgi:application --bind 0.0.0.0:8000"]