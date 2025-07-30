
FROM python:3.11-slim

# 安裝系統套件（包含 GDAL、PostGIS、GEOS 等）
RUN apt-get update && \
    apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev && \
    apt-get clean

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


WORKDIR /app


COPY . .


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000


CMD ["gunicorn", "calCrimes.wsgi:application", "--bind", "0.0.0.0:8000"]