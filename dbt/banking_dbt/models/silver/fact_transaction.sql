SELECT
    transaction_id,
    transaction_date,

    transaction_type,
    transaction_status,

    amount,
    currency,
    running_balance,

    payment_channel,
    payment_method,

    is_flagged_fraud,

    customer_id,
    account_id,
    credit_card_id,

    merchant_name,
    merchant_category,

    branch_id,

    _loaded_at

FROM {{ ref('stg_banking_transactions') }}
WHERE transaction_id IS NOT NULL