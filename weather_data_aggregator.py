import requests
import sqlite3
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
API_KEY = 'your_openweathermap_api_key'  # Ensure you replace this with your actual API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
INTERVAL = 3600  # 1 hour in seconds

def fetch_weather_data(city):
    """
    Fetch weather data from OpenWeatherMap API for a given city.

    Parameters:
    city (str): The name of the city to fetch the weather data for.

    Returns:
    dict: The weather data if the request is successful, None otherwise.
    """
    url = BASE_URL.format(city, API_KEY)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def extract_data(data, city):
    """
    Extract relevant data from the API response.

    Parameters:
    data (dict): The weather data from the API response.
    city (str): The name of the city.

    Returns:
    dict: A dictionary containing the extracted weather data.
    """
    if data:
        return {
            'timestamp': datetime.datetime.now().isoformat(sep=' '),
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main'].get('pressure', None),  # Use get to handle missing 'pressure'
            'weather_description': data['weather'][0]['description']
        }
    return None

def create_database():
    """
    Create SQLite database and table if they do not exist.
    """
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            pressure REAL,
            weather_description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(data):
    """
    Insert weather data into SQLite database.

    Parameters:
    data (dict): The weather data to be inserted into the database.
    """
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (timestamp, city, temperature, humidity, wind_speed, pressure, weather_description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['timestamp'], data['city'], data['temperature'], data['humidity'], data['wind_speed'], data['pressure'], data['weather_description']))
    conn.commit()
    conn.close()

def fetch_and_store_data(city, interval):
    """
    Fetch and store weather data at regular intervals.

    Parameters:
    city (str): The name of the city to fetch the weather data for.
    interval (int): The time interval (in seconds) between each data fetch.
    """
    create_database()
    while True:
        weather_data = fetch_weather_data(city)
        extracted_data = extract_data(weather_data, city)
        if extracted_data:
            insert_data(extracted_data)
        time.sleep(interval)

def fetch_all_data():
    """
    Fetch all weather data from SQLite database.

    Returns:
    DataFrame: A pandas DataFrame containing all the weather data.
    """
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    return df

def fetch_data_for_date_range(start_date, end_date):
    """
    Fetch weather data for a specific date range from SQLite database.

    Parameters:
    start_date (str): The start date (inclusive) in 'YYYY-MM-DD' format.
    end_date (str): The end date (inclusive) in 'YYYY-MM-DD' format.

    Returns:
    DataFrame: A pandas DataFrame containing the weather data for the specified date range.
    """
    conn = sqlite3.connect('weather_data.db')
    query = f"""
    SELECT * FROM weather 
    WHERE timestamp BETWEEN datetime('{start_date}') AND datetime('{end_date}', '+1 day')
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def analyze_data(df):
    """
    Perform basic statistical analysis on the weather data.

    Parameters:
    df (DataFrame): A pandas DataFrame containing the weather data.

    Returns:
    dict: A dictionary containing the average values for temperature, humidity, wind speed, and pressure.
    """
    analysis = {
        'average_temperature': df['temperature'].mean(),
        'average_humidity': df['humidity'].mean(),
        'average_wind_speed': df['wind_speed'].mean(),
        'average_pressure': df['pressure'].mean() if 'pressure' in df else None
    }
    return analysis

def visualize_data(df):
    """
    Visualize the weather data using box plots and heatmaps.

    Parameters:
    df (DataFrame): A pandas DataFrame containing the weather data.
    """
    sns.set(style="whitegrid")

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.set_index('timestamp', inplace=True)

    # Adjust figure size for better visibility on smaller screens
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Box plot for temperature
    sns.boxplot(data=df, y='temperature', ax=axes[0, 0])
    axes[0, 0].set_title('Temperature Distribution')
    axes[0, 0].set_ylabel('Temperature (K)')

    # Box plot for humidity
    sns.boxplot(data=df, y='humidity', ax=axes[0, 1])
    axes[0, 1].set_title('Humidity Distribution')
    axes[0, 1].set_ylabel('Humidity (%)')

    # Heatmap for wind speed
    pivot_data = df.pivot_table(values='wind_speed', index=df.index.date, columns=df.index.hour, aggfunc='mean')
    sns.heatmap(pivot_data, cmap="YlGnBu", ax=axes[1, 0])
    axes[1, 0].set_title('Wind Speed Heatmap')
    axes[1, 0].set_xlabel('Hour of Day')
    axes[1, 0].set_ylabel('Date')

    # Heatmap for pressure
    pivot_data = df.pivot_table(values='pressure', index=df.index.date, columns=df.index.hour, aggfunc='mean')
    sns.heatmap(pivot_data, cmap="YlGnBu", ax=axes[1, 1])
    axes[1, 1].set_title('Pressure Heatmap')
    axes[1, 1].set_xlabel('Hour of Day')
    axes[1, 1].set_ylabel('Date')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    city = input("Enter the city for which you want to fetch weather data: ")

    # Ensure API key is set
    if API_KEY == 'your_openweathermap_api_key':
        print("Please replace 'your_openweathermap_api_key' with your actual OpenWeatherMap API key.")
    else:
        # Create the database and fetch data
        create_database()

        # Fetch data once and analyze for testing
        weather_data = fetch_weather_data(city)
        if weather_data:
            extracted_data = extract_data(weather_data, city)
            if extracted_data:
                insert_data(extracted_data)
        
        # Fetch all data
        df = fetch_all_data()
        print(df)  # Display the data
        
        # Perform analysis on all data
        analysis = analyze_data(df)
        print(f"Average Temperature: {analysis['average_temperature']}")
        print(f"Average Humidity: {analysis['average_humidity']}")
        print(f"Average Wind Speed: {analysis['average_wind_speed']}")
        print(f"Average Pressure: {analysis['average_pressure']}")
        
        # Visualize all data
        visualize_data(df)

        # The date range prompt appears after closing the graph window
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        df_date_range = fetch_data_for_date_range(start_date, end_date)
        
        if not df_date_range.empty:
            print(df_date_range)  # Display data for the date range

            # Perform analysis on date range data
            analysis_date_range = analyze_data(df_date_range)
            print(f"Average Temperature (Date Range): {analysis_date_range['average_temperature']}")
            print(f"Average Humidity (Date Range): {analysis_date_range['average_humidity']}")
            print(f"Average Wind Speed (Date Range): {analysis_date_range['average_wind_speed']}")
            print(f"Average Pressure (Date Range): {analysis_date_range['average_pressure']}")
            
            # Visualize date range data
            visualize_data(df_date_range)
       
