WITH joined AS (
    SELECT 
        d.*, 
        w.*, 
        ABS(date_diff('minute', a.flightSCHED_DATETIME, w.timestamp)) AS diff
    FROM 
        rth_airport.departures d
        CROSS JOIN 
        rth_airport.weather w
),
ranked AS (
    SELECT 
        *, 
        ROW_NUMBER() OVER (PARTITION BY flightID ORDER BY diff) AS rank
    FROM 
        joined
)
SELECT * FROM ranked WHERE rank = 1