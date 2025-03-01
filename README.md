# Weather Dashboard

## Project Description
This Weather Dashboard is a web application that provides real-time weather updates for user-specified locations. The app utilizes the OpenWeatherMap API to fetch weather forecasts, including current weather, hourly forecasts, and a six-day forecast. The application is built using Flask for the backend and HTML, CSS, and JavaScript for the frontend. It also integrates Folium to generate interactive maps showing the searched locations.

## Features
- Search for a city's weather details.
- View current weather conditions, including temperature, humidity, and description.
- Get an hourly forecast for the next 24 hours.
- Display a six-day weather forecast with average daily temperatures.
- Interactive map showing the searched location.
- Search history stored in a database.

## Technologies Used
### Backend:
- Flask (Python Framework)
- SQLite (Database)
- SQLAlchemy (ORM for database management)
- Requests (Fetching weather data from OpenWeatherMap API)
- Logging (Error handling and debugging)

### Frontend:
- HTML, CSS (For structuring and styling)
- JavaScript (For interactivity and AJAX requests)
- Leaflet.js (For rendering interactive maps)
- Bootstrap (For responsive design)

## Project Structure
```
Weather_Dashboard/
│── static/
│   ├── Generated_map.html (Generated map visualization)
│   ├── style.css (CSS styles)
│   ├── temperature.png (Weather icon)
│── templates/
│   ├── history.html (Search history page)
│   ├── index.html (Homepage UI)
│   ├── map.html (Weather map page)
│   ├── results.html (Weather results display page)
│── app.py (Main Flask application)
│── config.py (Configuration file for the app)
│── database.db (SQLite database storing search history)
│── requirements.txt (Dependencies and required libraries)
│── README.md (Project documentation)
```

## Installation & Setup
### Clone the Repository
```sh
 git clone https://github.com/JohnssiManjunath3121/Weather_Dashboard
```

### Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Run the Application
```sh
python app.py
```

### Access the Application
Open your browser and go to:
```
http://127.0.0.1:5000/
```



