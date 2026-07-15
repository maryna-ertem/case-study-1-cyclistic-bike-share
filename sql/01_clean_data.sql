DROP TABLE IF EXISTS trips_clean CASCADE;

CREATE TABLE trips_clean AS
SELECT * FROM trips_raw;


-- Add the derived columns
ALTER TABLE trips_clean
    ADD COLUMN ride_length_min DOUBLE PRECISION,
    ADD COLUMN ride_length_bucket VARCHAR(20),
    ADD COLUMN bucket_sort_order INT,
    ADD COLUMN day_of_week VARCHAR(10),
    ADD COLUMN day_of_week_num INT,
    ADD COLUMN ride_month INT,
    ADD COLUMN ride_hour INT;

UPDATE trips_clean
SET
    ride_length_min = ROUND(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0, 2),
    ride_length_bucket = CASE
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 10 THEN '< 10 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 20 THEN '10 - 20 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 30 THEN '20 - 30 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 40 THEN '30 - 40 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 50 THEN '40 - 50 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 60 THEN '50 - 60 min'
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 90 THEN '1-1.5 hr'
        ELSE '1.5+ hr'
    END,
    bucket_sort_order = CASE
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 10 THEN 1
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 20 THEN 2
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 30 THEN 3
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 40 THEN 4
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 50 THEN 5
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 60 THEN 6
        WHEN EXTRACT(EPOCH FROM (ended_at - started_at))/60 < 90 THEN 7
        ELSE 8
    END,
    day_of_week = TO_CHAR(started_at, 'Day'),
    day_of_week_num = EXTRACT(ISODOW FROM started_at),
    ride_month = EXTRACT(MONTH FROM started_at),
    ride_hour = EXTRACT(HOUR FROM started_at);



-- EXPLORATION
-- Total row count
SELECT COUNT(*) AS total_rows FROM trips_clean;
-- 5,932,349 


-- Duplicate ride_ids
SELECT COUNT(*) - COUNT(DISTINCT ride_id) AS duplicate_ride_ids FROM trips_clean;
-- 35 duplicated


-- Missing timestamps
SELECT COUNT(*) FROM trips_clean WHERE started_at IS NULL OR ended_at IS NULL;
-- 0 missimg timestamps


-- Reversed/invalid timestamps (ride ends at or before it starts)
SELECT COUNT(*) FROM trips_clean WHERE ended_at <= started_at;
-- 29 invalid timestamps


-- Negative or null ride lengths (should mirror the reversed-timestamp count)
SELECT COUNT(*) FROM trips_clean WHERE ride_length_min IS NULL OR ride_length_min < 0;
-- 29 null/negative ride length


-- Distribution across duration buckets, to see where the long tail actually falls off
SELECT ride_length_bucket, bucket_sort_order, member_casual, COUNT(*) AS num_rides
FROM trips_clean
GROUP BY ride_length_bucket, bucket_sort_order, member_casual
ORDER BY bucket_sort_order, member_casual;

-- Missing ride_id
SELECT COUNT(*) FROM trips_clean WHERE ride_id IS NULL;
-- 0 missing rides




-- CLEANING QUERIES
-- Remove rows with reversed/invalid timestamps
DELETE FROM trips_clean WHERE ended_at <= started_at;

-- Remove rows with missing ride_id or missing timestamps
DELETE FROM trips_clean WHERE ride_id IS NULL OR started_at IS NULL OR ended_at IS NULL;

-- Remove duplicate ride_ids, keeping one copy of each (only run if duplicates > 0)
DELETE FROM trips_clean a USING trips_clean b
WHERE a.ctid < b.ctid AND a.ride_id = b.ride_id;



-- VERIFY
SELECT COUNT(*) AS total_rows_after_cleaning FROM trips_clean;
-- 5932285

SELECT COUNT(*) - COUNT(DISTINCT ride_id) AS duplicate_ride_ids FROM trips_clean; -- should be 0
-- 0

SELECT COUNT(*) FROM trips_clean WHERE ended_at <= started_at; -- should be 0
-- 0

SELECT COUNT(*) FROM trips_clean WHERE ride_length_min IS NULL; -- should be 0
-- 0




