Cyclistic Bike-Share Case Study: 
How does a bike-share navigate speedy success?

Tools: PostgreSQL · DBeaver · Python (pandas, seaborn, SQLAlchemy) 


1. ASK :: Business Task
Cyclistic is a Chicago-based bike-share program with over 5,800 bikes and 690+ stations. The director of marketing believes the company's future growth depends on converting casual riders (single-ride/day-pass customers) into annual members, since members are significantly more profitable.

This analysis answers: How do annual members and casual riders use Cyclistic bikes differently? 
The findings below are used to support three data-driven recommendations for a marketing campaign aimed at converting casual riders into members.


2. PREPARE :: Data Source
- Source: Divvy public trip data, published by Motivate International Inc. under license. Files were renamed locally (*-cyclistic-tripdata.csv) to match this case study's fictional "Cyclistic" branding.
- Time window: July 2025 – June 2026 (12 contiguous months)
- Volume: 5,932,349 rows loaded from 12 monthly CSV files
- Limitations:

No personally identifiable information is available — rides cannot be linked to individuals, so repeat casual riders or home addresses can't be determined.
Ride duration is measured only as time between dock-out and dock-in. It cannot distinguish a genuinely long ride from a bike left idle, lost, or malfunctioning — this is a stated limitation, not something addressed by cleaning.



3. PROCESS :: Data Cleaning & Processing
- Full SQL scripts: sql/01_clean_data.sql, sql/02_analysis.sql
- Steps:
    ~ Loaded all 12 months into a raw staging table (trips_raw) via PostgreSQL's \copy.
    ~ Checked for null timestamps, duplicate ride_ids, and rides with ended_at <= started_at (invalid/reversed timestamps).
    ~ Built a cleaned table (trips_clean) with derived fields: ride length in minutes, day of week, month, hour, and a ride-length duration bucket.
    ~ Rather than picking an arbitrary cutoff for "too long" rides, duration buckets were built first and inspected — confirming over 95% of casual rides and 99% of member rides complete within an hour, with anything past ~3 hours representing well under 1% of trips. This distribution justified treating very long rides as rare outliers rather than deleting them outright; they're retained in the data and separated out through bucketing rather than discarded.

4. ANALYZE :: Key Findings
    (a) Casual riders take longer trips; members take more total trips. Casual riders average 18.57 minutes per ride across 2,112,103 rides. Members average 12.07 minutes per ride across 3,814,650 rides — nearly double the ride volume, but 35% shorter on average.
    (b) Members show a clear two-peak commute pattern; casual riders don't. Member ride volume spikes sharply at 8am (278,840 rides) and 5pm (411,479 rides) — classic commute hours. Casual riders show one broad peak in the mid-to-late afternoon (3–5pm) with no morning spike at all.
    (c) Casual rides skew toward longer duration brackets. While both groups are concentrated under 20 minutes, casual riders have a visibly larger share of rides in the 20–60 minute and 1+ hour brackets, reinforcing the leisure-vs-commute distinction. 
    (d) Casual riders cluster at recreational/lakefront stations; members cluster downtown. Casual riders' top start stations are dominated by tourist and lakefront destinations — Navy Pier, DuSable Lake Shore Dr & Monroe St, Michigan Ave & Oak St, Millennium Park, Shedd Aquarium. Member top stations cluster around downtown/office areas.
    (e) Both groups favor electric bikes, casual riders slightly more so. Casual riders: 70.1% electric bike usage. Members: 66.3% electric bike usage — a modest but consistent difference.

5. SHARE :: Visuals
- Using python, generated four 150 DPI visualization assets directly alongside CSVs in /visuals:*
    ~ rides_by_day_of_week.png: Side-by-side subplots showcasing total rides vs. average durations.
    ~ rides_by_month.png**: Multi-line visualization of seasonal trends over the 12-month period.
    ~ rides_by_hour_of_day.png: Dual timeline illustrating member bimodal rush hour peaks vs. casual afternoon leisure bell-curves.
    ~ ride_length_buckets.png: Side-by-side comparative histogram validating trip duration segments.

6. ACT: Recommendations
- Target commute-adjacent membership tiers around downtown/office stations. Member usage clusters at these stations during clear 8am/5pm peaks — a work-commute-framed membership pitch fits existing behavior at these exact locations.
- Run a seasonal, lakefront-station campaign for casual riders. Since casual riders' top stations are clearly recreational (Navy Pier, Shedd Aquarium, Millennium Park), targeted signage and app prompts at these specific stations reach the highest concentration of convertible casual riders.
- Introduce a "long ride" or leisure-oriented membership tier. Casual riders' 54% longer average ride length and heavier share in the 20–90+ minute brackets suggests they aren't well-served by a commute-optimized membership. A tier priced and marketed around longer, occasional rides may convert more of them than the standard annual plan.



How to Reproduce

1. Set up PostgreSQL and load data
sudo systemctl start postgresql
psql -U cyclistic_user -d cyclistic_db -h localhost -f sql/01_clean_data.sql
psql -U cyclistic_user -d cyclistic_db -h localhost -f sql/02_analysis.sql

2. Set up Python environment
cd ~/Documents/cyclistic-case-study/visuals
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn psycopg2-binary sqlalchemy jupyterlab
python generate_charts.py


Project Structure

cyclistic-case-study/
├── .gitignore              # MUST HAVE: ignores /data/, venv/, and raw CSVs
├── requirements.txt        # For easy environment setup
├── README.md               # Documentation
├── sql/
│   ├── 01_clean_data.sql   # Creates table, handles staging & cleaning
│   └── 02_analysis.sql     # Performs analytical queries & aggregations
├── data/
│   ├── raw/                # Excluded from git; raw downloaded CSVs
│   └── processed/          # Excluded from git; cleaned tables/exported CSVs
├── scripts/
│   └── generate_charts.py  # Python script to compile visualizations
└── visuals/                # Strictly contains the exported .png charts



