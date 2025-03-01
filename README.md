Introduction
The Weather Dashboard is a web-based application that provides real-time weather updates for a specified city. The application fetches weather data from the OpenWeatherMap API and displays the current weather, an hourly forecast, and a six-day forecast. Additionally, it features an interactive map to visualize the searched location. The project is developed using Flask for the backend, HTML/CSS and JavaScript for the frontend, and SQLite for data storage.

Objectives
The primary goal of this project is to develop an interactive weather application that allows users to search for weather conditions of any city worldwide. The application aims to:
•	Fetch and display real-time weather data.
•	Provide an intuitive and user-friendly interface.
•	Store recent searches in a database for quick access.
•	Integrate an interactive map to visualize location-based weather data.
•	Ensure responsiveness across different devices.

Technologies Used
Frontend Technologies:
•	HTML, CSS, JavaScript: Used to design and structure the UI.
•	Leaflet.js: A JavaScript library for interactive maps, used to generate the weather location map.
Backend Technologies:
•	Flask: A Python-based web framework used to handle server-side logic and API interactions.
•	SQLite: A lightweight database to store search history.
•	OpenWeatherMap API: Provides real-time and forecasted weather data.

Implementation Details
Backend Implementation (Flask Server)
1.	Fetching Weather Data:
o	The /search route is responsible for receiving a city name from the user and querying the OpenWeatherMap API to fetch weather details.
o	The data is then processed to extract key information, including temperature, weather description, humidity, and forecasts.
2.	Database Management:
o	The application uses SQLite to store search history.
o	The Search History table maintains records of past searches to allow users quick access to previously searched locations.
o	A check ensures that duplicate searches for the same city on the same day are not stored.
3.	Interactive Map Generation:
o	The create_map() function in app.py generates an interactive map using Folium, entered on the searched city.
o	The map is saved as an HTML file in the static directory and rendered on the frontend.

Frontend Implementation
1.	User Interface (UI):
o	A clean and minimalistic UI that provides a search bar for city input.
o	Weather details, including the current temperature and conditions, are displayed dynamically.
o	Users can toggle between different map views (Street, Satellite, Terrain).
2.	Rendering Weather Data:
o	The /search route returns JSON data containing weather details, which are dynamically displayed on the webpage using JavaScript.
o	The forecasts are displayed in a structured manner, ensuring easy readability.
3.	Interactive Map:
o	Upon searching for a city, the location is plotted on the map using Leaflet.js.
o	The user can interact with the map to view weather conditions visually.

Features and Functionalities
•	Real-time Weather Updates: Fetches up-to-date weather data.
•	Hourly and 6-Day Forecasts: Provides detailed forecasts for informed decision-making.
•	Search History Storage: Saves recent searches for quick access.
•	Interactive Mapping: Displays a map view of the searched city with weather details.
•	Error Handling: Proper error messages are shown if an invalid city is searched, or the API request fails.

