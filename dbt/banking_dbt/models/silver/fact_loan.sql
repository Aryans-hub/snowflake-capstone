SELECT
    loan_id,
    customer_id,
    branch_id,

    loan_type,
    loan_amount,
    interest_rate,
    tenure_months,
    loan_status,

    _loaded_at

FROM {{ ref('stg_banking_transactions') }}
WHERE loan_id IS NOT NULL