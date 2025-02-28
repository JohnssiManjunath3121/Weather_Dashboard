import os
import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from flask import Flask, jsonify, render_template, request
import logging
import folium

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API Key for OpenWeatherMap (Replace with your own key if available)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "f1a1826b97302695cead326866fbabf1")

# Database setup
engine = create_engine(f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}", echo=False)
Base = declarative_base()

# SearchHistory Table Model
class SearchHistory(Base):
    __tablename__ = 'search_history'
    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the database tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Flask App
app = Flask(__name__)

# Ensure the 'static' folder exists for saving visualizations
if not os.path.exists('static'):
    os.makedirs('static')

# Fetch recent searches for the dropdown
@app.route('/recent-searches', methods=['GET'])
def recent_searches():
    """Fetch recent searches for the dropdown."""
    try:
        recent_searches = session.query(SearchHistory.city).distinct(SearchHistory.city).order_by(SearchHistory.timestamp.desc()).limit(5).all()
        return jsonify([search.city for search in recent_searches])
    except Exception as e:
        logging.error(f"Error fetching recent searches: {e}")
        return jsonify({'error': 'Could not fetch recent searches'}), 500

@app.route('/')
def index():
    """Render the homepage with the map."""
    logging.info("Rendering index page.")
    return render_template('map.html')

@app.route('/search', methods=['POST'])
def search():
    """Search for weather data for the given city."""
    try:
        city = request.json.get('city', '').strip()
        if not city:
            return jsonify({'error': 'City name cannot be empty.'}), 400

        # Fetch weather data
        weather_data = get_weather_data(city)
        if "error" in weather_data:
            return jsonify({'error': weather_data["error"]}), 400

        # Save search history
        save_search(city)

        # Extract current weather, hourly, and 6-day forecasts
        lat = weather_data['city']['coord']['lat']
        lon = weather_data['city']['coord']['lon']
        current = weather_data['list'][0]
        weather_description = current['weather'][0]['description'].capitalize()
        temperature = current['main']['temp']
        icon = current['weather'][0]['icon']
        humidity = current['main']['humidity']

        # Extract hourly forecast (next 8 periods ~24 hours)
        hourly_forecast = [
            {
                'time': item['dt_txt'],
                'temp': item['main']['temp'],
                'icon': item['weather'][0]['icon']
            }
            for item in weather_data['list'][:8]
        ]

        # Extract 6-day forecast
        six_day_forecast = []
        daily_temp = []
        prev_day = None
        for item in weather_data['list']:
            date = item['dt_txt'].split(' ')[0]
            if prev_day != date and daily_temp:
                six_day_forecast.append({
                    'date': prev_day,
                    'avg_temp': sum(temp[0] for temp in daily_temp) / len(daily_temp),
                    'icon': daily_temp[0][1]
                })
                daily_temp = []
            daily_temp.append((item['main']['temp'], item['weather'][0]['icon']))
            prev_day = date
        if daily_temp:
            six_day_forecast.append({
                'date': prev_day,
                'avg_temp': sum(temp[0] for temp in daily_temp) / len(daily_temp),
                'icon': daily_temp[0][1]
            })

        # Generate a map centered on the city
        create_map(lat, lon, weather_description, temperature)

        return jsonify({
            'lat': lat,
            'lon': lon,
            'weather': weather_description,
            'temperature': temperature,
            'icon': icon,
            'humidity': humidity,
            'hourly_forecast': hourly_forecast,
            'six_day_forecast': six_day_forecast
        })
    except Exception as e:
        logging.error(f"Error processing search request: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/history')
def history():
    """Render the search history page."""
    logging.info("Rendering search history page.")
    searches = session.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).all()
    return render_template('history.html', searches=searches)

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        logging.info(f"Fetching weather data for city: {city}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for city '{city}': {e}")
        return {"error": f"Could not retrieve data for {city}."}

def save_search(city):
    """Save search record to the database, avoiding duplicates for the same day."""
    try:
        # Check if the city was already searched today
        today = datetime.utcnow().date()
        existing_search = session.query(SearchHistory).filter(
            SearchHistory.city == city,
            SearchHistory.timestamp >= datetime(today.year, today.month, today.day)
        ).first()

        if existing_search:
            logging.info(f"Search for '{city}' already exists for today. Skipping save.")
            return  # Don't save duplicate entries for the same city on the same day

        # If no existing search, save the new search
        new_search = SearchHistory(city=city)
        session.add(new_search)
        session.commit()
        logging.info(f"Search for '{city}' saved to database.")
    except Exception as e:
        logging.error(f"Error saving search to database: {e}")
        session.rollback()

def create_map(lat, lon, weather_description, temperature):
    """Generate a map with the weather location and save it as an HTML file."""
    try:
         # Generate popup information
        popup_info = f"Weather: {weather_description}, Temp: {temperature}°C"

        # Log the map creation attempt
        logging.info(f"Generating weather map for location: ({lat}, {lon})")

        # Create the folium map
        weather_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup=popup_info).add_to(weather_map)

        # Construct the correct path to the static folder
        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        output_path = os.path.join(static_folder, 'Generated_map.html')

        # Save the generated map
        weather_map.save(output_path)
        logging.info(f"Weather map saved as '{output_path}'.")
    except Exception as e:
        logging.error(f"Error generating map: {e}")

if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(debug=True)
