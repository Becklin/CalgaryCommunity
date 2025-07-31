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
   # Install system GDAL first (required for GeoDjango)
   # macOS
   brew install gdal
   # Ubuntu/Debian
   sudo apt install gdal-bin libgdal-dev
   # Windows
   # Install OSGeo4W or GDAL binaries manually

   # Then install Python dependencies
   pip install -r requirements.txt
   ```

3. Development - Set up PostgreSQL and PostGIS:

   - Install PostgreSQL.
   - Enable PostGIS extension.
   - Run PostgreSQL server.

4. Run the project:

   ```bash
   python manage.py migrate
   python manage.py add_income_to_community ...
   python manage.py runserver
   ```

5. Access the application:

   Development - `http://127.0.0.1:8000/` in your browser.

## Deployment

1. **Backend endpoint** - https://calcommunity.onrender.com/
2. **Frontend** - https://calgary-community-frontend.vercel.app/
   GitHub - https://github.com/Becklin/calgary-community-frontend
3. **Database** - https://supabase.com/dashboard/project/flsgrbtpuhbgdpsokfss
   - Use IPv4 for Supabase connection because Render does not support connecting to the database with IPv6.
   - Supabase provides IPv6 only on paid plans.
   - In Supabase, enable the PostGIS extension for your database before running the application.
> **Note:**
> - Set `DJANGO_DEBUG` to `True` to troubleshoot in production.
> - A Docker image is used on Render to avoid errors caused by GDAL installation.
> - Create docker image
   ```bash
   Docker login
   Docker build -t DockerAccount/imageName .
   Docker push DockerAccount/imageName
   ```

## Usage

- Explore the different communities by interacting with the map.
- Rank communities based on services, population, or other criteria.
- View detailed data about selected communities.

## APIs

**Community boundaries**
- https://data.calgary.ca/resource/surr-xmvs.json
- https://dev.socrata.com/foundry/data.calgary.ca/surr-xmvs

**Community services**
- https://data.calgary.ca/resource/x34e-bcjz.json

**Income**
- https://data.calgary.ca/resource/wj3a-wgmh.json

**Police Department**
- https://data.calgary.ca/resource/ap4r-bav3.json

**Parks**
- https://data.calgary.ca/resource/kami-qbfh.json

**Census by Community**
- https://data.calgary.ca/resource/rkfr-buzb.json
