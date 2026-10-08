SELECT DISTINCT
    credit_card_id,
    customer_id,
    card_type,
    card_network,
    credit_limit,
    card_status
FROM {{ ref('stg_banking_transactions') }}
WHERE credit_card_id IS NOT NULL