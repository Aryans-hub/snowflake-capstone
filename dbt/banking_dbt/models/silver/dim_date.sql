WITH date_range AS (

    SELECT
        MIN(transaction_date) AS min_date,
        MAX(transaction_date) AS max_date
    FROM {{ ref('stg_banking_transactions') }}

),

dates AS (

    SELECT
        DATEADD(
            DAY,
            SEQ4(),
            min_date
        ) AS date_day

    FROM date_range,
         TABLE(GENERATOR(ROWCOUNT => 10000))

    WHERE DATEADD(
        DAY,
        SEQ4(),
        min_date
    ) <= max_date

)

SELECT
    date_day AS date_key,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    MONTHNAME(date_day) AS month_name,
    QUARTER(date_day) AS quarter,
    DAY(date_day) AS day,
    DAYOFWEEK(date_day) AS day_of_week,
    DAYNAME(date_day) AS day_name

FROM dates