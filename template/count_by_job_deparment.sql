SELECT
    d.deparment,
    j.job,
    COUNT(CASE WHEN EXTRACT(MONTH FROM CAST(h.datetime as date)) BETWEEN 1 AND 3 THEN 1 ELSE NULL END) AS Q1,
    COUNT(CASE WHEN EXTRACT(MONTH FROM CAST(h.datetime as date)) BETWEEN 4 AND 6 THEN 1 ELSE NULL END) AS Q2,
    COUNT(CASE WHEN EXTRACT(MONTH FROM CAST(h.datetime as date)) BETWEEN 7 AND 9 THEN 1 ELSE NULL END) AS Q3,
    COUNT(CASE WHEN EXTRACT(MONTH FROM CAST(h.datetime as date)) BETWEEN 10 AND 12 THEN 1 ELSE NULL END) AS Q4
FROM
    public.hiredemployee h
    INNER JOIN public.job j ON h.job_id = j.id
    INNER JOIN public.deparment d ON h.deparment_id = d.id
WHERE
    CAST(h.datetime as date) IS NOT NULL
    AND EXTRACT(YEAR FROM cast(h.datetime as date)) = {{ select_year }}  
GROUP BY
    d.deparment,
    j.job
ORDER BY
    d.deparment,
    j.job;