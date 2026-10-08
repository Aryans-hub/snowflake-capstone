SELECT DISTINCT
    account_id,
    customer_id,
    account_type,
    account_open_date,
    account_status,
    branch_id
FROM {{ ref('stg_banking_transactions') }}
WHERE account_id IS NOT NULL