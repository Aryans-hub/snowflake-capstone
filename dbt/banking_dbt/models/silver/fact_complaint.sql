SELECT
    complaint_id,
    customer_id,
    branch_id,

    complaint_category,
    complaint_priority,
    complaint_status,

    _loaded_at

FROM {{ ref('stg_banking_transactions') }}
WHERE complaint_id IS NOT NULL
