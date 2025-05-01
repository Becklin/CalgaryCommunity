# CalgaryCommunity

A GIS-based web application that provides community-ranking in Calgary. This project allows users to rank communities based on various metrics, and shows those locations on a map.

## Features

- **Map Visualization**: Interactive map to display different communities in Calgary using React Leaflet.
- **Community Data**: Provides information about services and statistics such as crime rates, population, and income distribution.
- **Geospatial Data Integration**: Utilizes Django and GeoDjango for handling spatial data efficiently.
- **PostgreSQL & PostGIS**: Backend powered by PostgreSQL with PostGIS for geospatial queries.

## Technologies Used

- **Frontend**: React, React Leaflet
- **Backend**: Django, GeoDjango
- **Database**: PostgreSQL with PostGIS extension

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Becklin/CalgaryCommunity.git
   cd CalgaryCommunity
   ```

2. Install dependencies:

   ```bash
   pip install gdal
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL and PostGIS:

   - Install PostgreSQL.
   - Enable PostGIS extension.
   - run Postgresql

4. Run the project:

   ```bash
   python manage.py migrate
   python manage.py add_income_to_community ...
   python manage.py runserver
   ```

   ```bash
   npm run dev
   ```

5. Access the application:

   Visit `http://127.0.0.1:8000/` in your browser.

## Usage

- Explore the different communities by interacting with the map.
- Rank communities based on services, population, or other criteria.
- View detailed data about selected communities.

## Future Improvements

- Add more layers of data like traffic, air quality, etc.
- Improve mobile responsiveness.
- Host on Heroku

## APIs
   ```community boundaries
   ```
- https://data.calgary.ca/resource/surr-xmvs.json
- https://dev.socrata.com/foundry/data.calgary.ca/surr-xmvs

   ```community services
   ```
- https://data.calgary.ca/resource/x34e-bcjz.json

   ```Income
   ```
- https://data.calgary.ca/resource/wj3a-wgmh.json

   ```Police Department
   ```
- https://data.calgary.ca/resource/ap4r-bav3.json
   ```Parks
   ```
- https://data.calgary.ca/resource/kami-qbfh.json

🎯 關聯邏輯（先後順序）
先定義 models.py 中的模型（比如 Community）

執行 makemigrations 和 migrate → 在資料庫中建立 community 這個表格和欄位。

之後才執行 load_community_csv → 把 CSV 中的資料存入這個 community 表。

如果沒先執行 migrate，資料表不存在，CSV 載入就會報錯（例如：table does not exist）。

