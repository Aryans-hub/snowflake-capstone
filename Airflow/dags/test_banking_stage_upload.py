from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="test_banking_stage_upload",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["banking", "snowflake", "test"],
) as dag:
    upload_file = SQLExecuteQueryOperator(
        task_id="upload_file",
        conn_id="snowflake_conn",
        sql="""
            PUT 'file:///opt/airflow/data/input/banking_datset_1.csv'
            @CAPSTONE_DB.BRONZE.BANKING_STAGE
            AUTO_COMPRESS=TRUE
            OVERWRITE=TRUE;
        """,
    )
