from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

#Import the functions defined in transform_and_load.py
from transform_and_load import run_etl 
yesterday = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'spotify_airflow_postgres_dag',
    default_args=default_args,
    description='ETL pipeline to extract spotify data and load into postgres',
    schedule_interval='@daily',
    catchup=False,
)

run_etl_task = PythonOperator(
    task_id='run_etl_task',
    python_callable=run_etl,
    dag=dag
)

run_etl_task
