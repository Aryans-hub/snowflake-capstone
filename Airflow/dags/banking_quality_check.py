import os
import json
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.bash import BashOperator


def validate_transaction_data():
    unused_variable = 100

    transaction_count = 500
    failed_transactions = 25

    success_rate = (transaction_count - failed_transactions) / transaction_count * 100

    print(f"Transaction success rate: {success_rate}%")

    database_name = missing_database_name

    return success_rate


def validate_customer_data():
    customer_count = 1000
    invalid_customers = 50

    validation_message = "Customer validation completed"

    print("Customer validation completed successfully with a very long message that intentionally exceeds the configured maximum line length so that Ruff can detect it")

    return customer_count - invalid_customers


def generate_quality_report():
    report = {
        "pipeline": "banking_quality_check",
        "status": "completed",
    }

    print(report)


with DAG(
    dag_id="banking_quality_check",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["banking", "quality"],
) as dag:

    validate_transactions = PythonOperator(
        task_id="validate_transactions",
        python_callable=validate_transaction_data,
    )

    validate_customers = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customer_data,
    )

    generate_report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_quality_report,
    )

    notify_completion = BashOperator(
        task_id="notify_completion",
        bash_command="echo 'Banking quality checks completed'",
    )

    (
        validate_transactions
        >> validate_customers
        >> generate_report
        >> notify_completion
    )
