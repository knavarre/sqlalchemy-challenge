# Hawaii Climate Analysis
By Kiana Navarre

**Programming Language Used: SQLAlchemy ORM queries, Flask,  Python, Pandas, Matplotlib**

## Description
In this project, a climate analysis is performed for a theoretical trip to Honolulu, Hawaii.  This analysis is divided into 2 main sections: 
1. Analysis and Exploration of Climate Data 
2. Climate App Creation

## Analysis and Exploration of Climate Data
In this section of the analysis, SQLAlchemy is used to connect to a provided SQLite database and the auto_base() function is used to reflect the station and measurement tables (found in the Resources folder) into classes. The following analyses were then performed: 

### Precipitation Analysis:
- Using the most recent date in the dataset given, the precipitation data for the previous 12 months was queried for and plotted using Matplotlib. 
- Pandas was then used to print the summary statistics for the precipitation data. 

### Station Analysis
- Queries were used to:
  - calculate the number of total stations in the dataset
  - determine the most active stations (the stations that have the most rows)
  - calculate the lowest, highest, and average temperatures that filters on the most active station ID 
  - retrieve the previous 12 months of temperature observation data (TOBS)
- A plot of temperature opservation data frequency was generated using Matplotlib. 

## Climate App Creation
In this section of the analysis, a Flask API is created based on the queries in the previous section.  From the homepage, the following routes are listed: 
- /api/v1.0/precipitation
  - retrieves last 12 months of precipitation (prcp) data as a dictionary using date as the key and prcp as the value
- /api/v1.0/stations
  - returns a JSON list of stations from the dataset
- /api/v1.0/tobs
  - returns a JSON list of temperature observations for the previous year
- /api/v1.0/input_start_date
  - returns the minimum, maximum, and average temperature for a specified start date to the end of the dataset. 
- /api/v1.0/input_start_date/input_end_date
  - returns the minimum, maximum, and average temperature for a specified start date to a specified end date.