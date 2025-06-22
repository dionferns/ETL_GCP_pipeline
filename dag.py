from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 21),
    'depends_on_past': False,
    'email': ['dionfernandes5@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('employee_data',
          default_args=default_args,
          description='Runs an external Python script',
          schedule_interval='@daily',
          catchup=False)

with dag:
    run_script_task = BashOperator(
        task_id='extract_data',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py',
    )
    start_pipeline = CloudDataFusionStartPipelineOperator(
    location="us-central1",
    pipeline_name="etl-pipeline2",
    instance_name="datafusion-dev",
    pipeline_timeout=1000,
    task_id="start_datafusion_pipeline",
)

run_script_task >> start_pipeline
# This dag, will run the extract.py file which is loaded into the bucket/dags/scripts/extract.py, which will create the dummy data, and load it into the gcs bucket. 