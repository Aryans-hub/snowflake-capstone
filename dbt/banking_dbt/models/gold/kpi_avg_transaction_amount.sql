SELECT
    transaction_type,
    AVG(amount) AS average_transaction_amount
FROM {{ ref('fact_transaction') }}
WHERE transaction_type IS NOT NULL
  AND amount IS NOT NULL
GROUP BY transaction_type
ORDER BY average_transaction_amount DESC