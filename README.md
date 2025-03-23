# spotify_airflow_postgres
This project showcases an end-to-end ETL (Extract, Transform, Load) pipeline that extracts data from the Spotify API using Python, transforms the data, loads it into a PostgreSQL database and orchestrate the ETL process using Apache Airflow. This demonstrates practical data engineering skills using real-world data.

## Overview
This simple ETL pipeline does the following:
### 1. Extract: 
[Link to extract.py](https://github.com/Oreoluwa100/spotify_airflow_postgres/blob/main/extract.py)

This extracts data from Spotify's Web API for a specific artist (e.g., "Tems"). It involves retrieving an access token, searching for the artist ID, collecting artist details, album information, album tracks, and top tracks.

### 2. Transform and Load:
[Link to transform_and_load.py](https://github.com/Oreoluwa100/spotify_airflow_postgres/blob/main/transform_and_load.py)

This includes transformations such as handling type conversions (e.g., transforming release dates into datetime objects and converting track durations from milliseconds to minutes) and structure adjustments. The data is then loaded into a PostgreSQL database by inserting records into relevant tables using Python’s psycopg2 library.

### 3. Orchestration:
[Link to dag file](https://github.com/Oreoluwa100/spotify_airflow_postgres/blob/main/spotify_airflow_postgres_dag.py)

The ETL process is orchestrated using Apache Airflow, which schedules and automates the workflow to run daily. 

### Technologies Used:

Spotify API: To fetch artist, album and track data.

PostgreSQL: To store the extracted data.

Apache Airflow: To orchestrate the ETL pipeline.

Python: For scripting the ETL process

### Libraries:
requests: To interact with the Spotify API.

psycopg2: To connect to PostgreSQL.

python-dotenv: To manage environment variables.

apache-airflow: To schedule and run the ETL pipeline.

