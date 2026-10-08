SELECT DISTINCT
    merchant_name,
    merchant_category
FROM {{ ref('stg_banking_transactions') }}
WHERE merchant_name IS NOT NULL