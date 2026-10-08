from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


SNOWFLAKE_CONN_ID = "snowflake_conn"

CSV_FILE = "/opt/airflow/data/input/banking_datset_1.csv"


with DAG(
    dag_id="banking_bronze_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["banking", "bronze", "snowflake"],
) as dag:

    upload_to_stage = SQLExecuteQueryOperator(
        task_id="upload_to_stage",
        conn_id=SNOWFLAKE_CONN_ID,
        sql=f"""
            PUT 'file://{CSV_FILE}'
            @CAPSTONE_DB.BRONZE.BANKING_STAGE
            AUTO_COMPRESS=TRUE
            OVERWRITE=TRUE;
        """,
    )

    load_bronze = SQLExecuteQueryOperator(
        task_id="load_bronze",
        conn_id=SNOWFLAKE_CONN_ID,
        sql="""
            COPY INTO CAPSTONE_DB.BRONZE.RAW_BANKING_DATA
            (
                transaction_id,
                transaction_date,
                transaction_type,
                amount,
                currency,
                transaction_status,
                payment_channel,
                payment_method,
                running_balance,
                is_flagged_fraud,
                merchant_name,
                merchant_category,
                customer_id,
                customer_name,
                customer_dob,
                customer_gender,
                customer_email,
                customer_phone,
                customer_city,
                customer_country,
                customer_segment,
                kyc_status,
                customer_annual_income,
                credit_score,
                account_id,
                account_type,
                account_open_date,
                account_status,
                branch_id,
                branch_name,
                credit_card_id,
                card_type,
                card_network,
                credit_limit,
                card_status,
                loan_id,
                loan_type,
                loan_amount,
                interest_rate,
                tenure_months,
                loan_status,
                complaint_id,
                complaint_category,
                complaint_priority,
                complaint_status
            )
            FROM @CAPSTONE_DB.BRONZE.BANKING_STAGE
            FILE_FORMAT = (
                FORMAT_NAME = 'CAPSTONE_DB.BRONZE.BANKING_CSV_FORMAT'
            )
            ON_ERROR = 'ABORT_STATEMENT';
        """,
    )

    upload_to_stage >> load_bronze