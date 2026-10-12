from datetime import datetime

from airflow.providers.snowflake.operators.snowflake import SQLExecuteQueryOperator

from airflow import DAG

with DAG(
    dag_id="test_snowflake_connection",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    test_connection = SQLExecuteQueryOperator(
        task_id="test_connection",
        conn_id="snowflake_conn",
        sql="SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA();",
    )
