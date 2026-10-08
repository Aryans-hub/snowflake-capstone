SELECT DISTINCT
    branch_id,
    branch_name
FROM {{ ref('stg_banking_transactions') }}
WHERE branch_id IS NOT NULL