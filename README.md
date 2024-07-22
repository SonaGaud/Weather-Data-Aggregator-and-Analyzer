**Setup Instructions**

**Prerequisites**

    •	Python 3.6 or higher
    
    •	SQLite3 (comes pre-installed with Python)
    
    •	Internet connection to fetch weather data
    
    •	OpenWeatherMap API key (sign up at OpenWeatherMap to get your API key)

**Required Python Libraries**

    •	requests
    
    •	sqlite3
    
    •	pandas
    
    •	matplotlib
    
    •	seaborn

**You can install the required libraries using the following command:**

    pip install requests pandas matplotlib seaborn
      
**Clone or Download the Repository**

    Clone the repository or download the source code files to your local machine.

**Configuration**

    1.	Open the source code file weather_data_aggregator.py.
    
    2.	Replace your_openweathermap_api_key with your actual OpenWeatherMap API key.
   
**Running the Application**

**1.Fetch and Store Data:**

    o	Open your terminal or command prompt.
    
    o	Navigate to the directory where the weather_data_aggregator.py file is located.
    
    o	Run the script:
    
              python weather_data_aggregator.py
          
        	  Enter the city name when prompted

**2.Perform Data Analysis:**

    o	The script will fetch weather data for the specified city and store it in a SQLite database (weather_data.db).
    
    o	The script will print the data fetched from the database and display average values for temperature, humidity, wind speed, and pressure.
    
    o	The script will prompt you to enter a date range to perform analysis on data within that range.
    
    o	The script will print the data and average values for the specified date range and display visualizations.

**3.Visualization**

  •	**The script will display visualizations including:**
  
    o	Box plots for temperature and humidity distribution.
    
    o	Heatmaps for wind speed and pressure over time.
