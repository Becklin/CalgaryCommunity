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
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL and PostGIS:

   - Install PostgreSQL.
   - Enable PostGIS extension.

4. Run the project:

   ```bash
   python manage.py migrate
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
