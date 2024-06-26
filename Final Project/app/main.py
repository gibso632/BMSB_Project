# Import necessary libraries
from flask import Flask, jsonify
import os
import psycopg2

# Set up variable for constructing Flask application
app = Flask(__name__)

# Set variables equal to connections
database = 'gis5572'
user = 'postgres'
password = 'Hyderabad43%'
host = '35.238.64.215'
port = '5432'

# Set variables for additions to GeoJSON for formatting
gj_start = '{"type":"FeatureCollection", "features":['
gj_end = ']}'

@app.route('/')
def home():
    return "Final Project GIS5572"

# Set up application to perform a function
@app.route('/BMSB_rank')
def mn_cities_rank():
    
    # Connect to SDE database
    conn = psycopg2.connect(
        database = database,
        user = user,
        password = password,
        host = host,
        port = port
    )
    
    # Set up cursor
    cursor = conn.cursor()
    
    # Create a variable for a query to extract the GeoJSON
    query = "SELECT JSON_AGG(ST_AsGeoJSON(mn_cities_2_ranked_wgs84)) FROM mn_cities_2_ranked_wgs84"
    
    # Execute the query
    cursor.execute(query)
    
    # Restructure the GeoJSON into correct format
    mn_cities_rank = (str(cursor.fetchall())).replace("\'","").replace("[([","").replace("],)]","")
    mn_cities_rank_final = gj_start + mn_cities_rank + gj_end
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    # Return GeoJSON
    return mn_cities_rank_final

# Run the application
if __name__ == "__main__":
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = int(os.environ.get("PORT",8080))
    )
