WITH source_data AS (

    SELECT *
    FROM CAPSTONE_DB.BRONZE.RAW_BANKING_DATA

)

SELECT
    transaction_id,
    TRY_TO_DATE(transaction_date) AS transaction_date,
    transaction_type,
    TRY_TO_DECIMAL(amount, 18, 2) AS amount,
    currency,
    transaction_status,
    payment_channel,
    payment_method,
    TRY_TO_DECIMAL(running_balance, 18, 2) AS running_balance,
    TRY_TO_BOOLEAN(is_flagged_fraud) AS is_flagged_fraud,

    merchant_name,
    merchant_category,

    customer_id,
    customer_name,
    TRY_TO_DATE(customer_dob) AS customer_dob,
    customer_gender,
    customer_email,
    customer_phone,
    customer_city,
    customer_country,
    customer_segment,
    kyc_status,
    TRY_TO_DECIMAL(customer_annual_income, 18, 2) AS customer_annual_income,
    TRY_TO_NUMBER(credit_score) AS credit_score,

    account_id,
    account_type,
    TRY_TO_DATE(account_open_date) AS account_open_date,
    account_status,

    branch_id,
    branch_name,

    credit_card_id,
    card_type,
    card_network,
    TRY_TO_DECIMAL(credit_limit, 18, 2) AS credit_limit,
    card_status,

    loan_id,
    loan_type,
    TRY_TO_DECIMAL(loan_amount, 18, 2) AS loan_amount,
    TRY_TO_DECIMAL(interest_rate, 18, 4) AS interest_rate,
    TRY_TO_NUMBER(tenure_months) AS tenure_months,
    loan_status,

    complaint_id,
    complaint_category,
    complaint_priority,
    complaint_status,

    _loaded_at

FROM source_data