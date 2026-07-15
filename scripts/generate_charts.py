import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set consistent, professional styling
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8,
    'xtick.color': '#333333',
    'ytick.color': '#333333'
})

# Brand colors: Members (Navy/Blue), Casuals (Coral/Orange)
PALETTE = {"member": "#1a5f7a", "casual": "#f26419"}

# Resolve relative paths dynamically
# SCRIPT_DIR is .../cyclistic-case-study/scripts
SCRIPT_DIR = Path(__file__).resolve().parent
# BASE_DIR is .../cyclistic-case-study
BASE_DIR = SCRIPT_DIR.parent

DATA_DIR = BASE_DIR / "data" / "raw"
VISUALS_DIR = BASE_DIR / "visuals"

# Ensure the visuals output directory exists
VISUALS_DIR.mkdir(parents=True, exist_ok=True)


def plot_day_of_week():
    """Generates a side-by-side subplot of weekly ride volume and average duration."""
    csv_path = DATA_DIR / "rides-by-day-of-week.csv"
    df = pd.read_csv(csv_path)
    
    # Strip any trailing whitespace from SQL output (e.g. 'Monday    ' -> 'Monday')
    df['day_of_week'] = df['day_of_week'].str.strip()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Subplot 1: Total Rides by Day of Week
    sns.barplot(
        data=df, x='day_of_week', y='num_rides', hue='member_casual', 
        palette=PALETTE, ax=axes[0]
    )
    axes[0].set_title("Total Rides by Day of Week", fontsize=14, fontweight='bold', pad=15)
    axes[0].set_xlabel("Day of Week", fontsize=11)
    axes[0].set_ylabel("Number of Rides", fontsize=11)
    axes[0].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    axes[0].legend(title="User Type")

    # Subplot 2: Average Ride Length by Day of Week
    sns.barplot(
        data=df, x='day_of_week', y='avg_ride_min', hue='member_casual', 
        palette=PALETTE, ax=axes[1]
    )
    axes[1].set_title("Average Ride Length by Day of Week", fontsize=14, fontweight='bold', pad=15)
    axes[1].set_xlabel("Day of Week", fontsize=11)
    axes[1].set_ylabel("Average Duration (Minutes)", fontsize=11)
    axes[1].legend(title="User Type")
    
    plt.tight_layout()
    
    # Save directly to visuals/
    output_path = VISUALS_DIR / "rides_by_day_of_week.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_path.name}")


def plot_monthly_seasonality():
    """Generates a line chart showing seasonal ride volume trends."""
    csv_path = DATA_DIR / "rides-by-month.csv"
    df = pd.read_csv(csv_path)
    
    months_map = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }
    df['month_name'] = df['ride_month'].map(months_map)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=df, x='month_name', y='num_rides', hue='member_casual', 
        palette=PALETTE, marker='o', linewidth=2.5, markersize=8
    )
    
    plt.title("Seasonal Riding Patterns (Rides per Month)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Number of Rides", fontsize=11)
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend(title="User Type")
    
    plt.tight_layout()
    
    # Save directly to visuals/
    output_path = VISUALS_DIR / "rides_by_month.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_path.name}")


def plot_hourly_demand():
    """Generates a line chart displaying system usage hourly fluctuations."""
    csv_path = DATA_DIR / "rides-by-hour-of-day.csv"
    df = pd.read_csv(csv_path)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=df, x='ride_hour', y='num_rides', hue='member_casual', 
        palette=PALETTE, linewidth=2.5
    )
    
    plt.xticks(range(0, 24))
    plt.title("Hourly Ride Volume (24-Hour Cycle)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Hour of the Day (00:00 - 23:00)", fontsize=11)
    plt.ylabel("Number of Rides", fontsize=11)
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend(title="User Type")
    
    # Highlight classic commute rush hours (7-9 AM, 4-6 PM)
    plt.axvspan(7, 9, color='gray', alpha=0.15, label='Morning Rush')
    plt.axvspan(16, 18, color='gray', alpha=0.15, label='Evening Rush')
    
    plt.tight_layout()
    
    # Save directly to visuals/
    output_path = VISUALS_DIR / "rides_by_hour_of_day.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_path.name}")


def plot_duration_buckets():
    """Generates a bar plot showing the distribution of ride lengths."""
    csv_path = DATA_DIR / "duration-distribution.csv"
    df = pd.read_csv(csv_path)
    
    # Keep logical progression of trip duration sorted by SQL order
    df = df.sort_values('bucket_sort_order')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df, x='ride_length_bucket', y='num_rides', hue='member_casual', 
        palette=PALETTE
    )
    
    plt.title("Distribution of Ride Durations", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Trip Duration Bucket", fontsize=11)
    plt.ylabel("Number of Rides", fontsize=11)
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend(title="User Type")
    plt.xticks(rotation=15)
    
    plt.tight_layout()
    
    # Save directly to visuals/
    output_path = VISUALS_DIR / "ride_length_buckets.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_path.name}")


if __name__ == "__main__":
    print(f"Project Root Detected: {BASE_DIR}")
    print(f"Reading CSV datasets from: {DATA_DIR}")
    print(f"Writing visualization output to: {VISUALS_DIR}\n")
    
    # Safety check
    if not DATA_DIR.exists():
        print(f"❌ Error: The directory '{DATA_DIR}' does not exist. Please place your CSV files there.")
    else:
        plot_day_of_week()
        plot_monthly_seasonality()
        plot_hourly_demand()
        plot_duration_buckets()
        print("\n🎉 Success! All visualizations are saved in /visuals.")
