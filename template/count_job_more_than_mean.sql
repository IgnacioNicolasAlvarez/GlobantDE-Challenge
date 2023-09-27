WITH department_avg AS (
    SELECT
        deparment_id,
        AVG(CASE WHEN EXTRACT(YEAR FROM cast(datetime as date)) = {{ select_year }} THEN 1 ELSE 0 END) AS avg_{{ select_year }}
    FROM public.hiredemployee
    GROUP BY deparment_id
),
department_hires AS (
    SELECT
        h.deparment_id,
        d.deparment AS department,
        COUNT(*) AS hired
    FROM public.hiredemployee h
    JOIN public.deparment d ON h.deparment_id = d.id
    WHERE EXTRACT(YEAR FROM cast(h.datetime as date)) = {{ select_year }}
    GROUP BY h.deparment_id, d.deparment
)
SELECT
    d.id,
    d.deparment AS name,
    dh.hired
FROM department_hires dh
JOIN department_avg da ON dh.deparment_id = da.deparment_id
JOIN public.deparment d ON dh.deparment_id = d.id
WHERE dh.hired > da.avg_{{ select_year }}
ORDER BY dh.hired DESC;