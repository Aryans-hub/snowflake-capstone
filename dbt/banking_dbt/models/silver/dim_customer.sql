SELECT DISTINCT
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
    credit_score
FROM {{ ref('stg_banking_transactions') }}
WHERE customer_id IS NOT NULL