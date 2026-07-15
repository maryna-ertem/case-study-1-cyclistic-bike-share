-- Create a filtered view for duration-based analysis, keeping trips_clean itself untouched:
CREATE VIEW trips_analysis AS
SELECT * FROM trips_clean WHERE ride_length_min <= 180;


-- Overall ride length stats 
SELECT 
    member_casual, 
    ROUND(AVG(ride_length_min)::numeric, 2) AS avg_ride_min, 
    COUNT(*) AS total_rides 
FROM trips_analysis
GROUP BY member_casual

-- Rides by the day of week
SELECT 
	member_casual, day_of_week, day_of_week_num,
	COUNT(*) AS num_rides,
	ROUND(AVG(ride_length_min)::numeric, 2) AS avg_ride_min
FROM trips_analysis
GROUP BY member_casual, day_of_week, day_of_week_num
ORDER BY day_of_week_num;


-- Rides by month
SELECT 
	member_casual, ride_month,
	COUNT(*) AS num_rides
FROM trips_analysis
GROUP BY member_casual, ride_month
ORDER BY ride_month;


-- Rides by hour of day
SELECT
	member_casual, ride_hour, 
	COUNT(*) AS num_rides
FROM trips_analysis
GROUP BY member_casual, ride_hour
ORDER BY ride_hour;



