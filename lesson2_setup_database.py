"""
Lesson 2: SQL Database Setup for Tourism Data
Normalizes CSV data into a relational database structure
"""

import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('tourism.db')
cursor = conn.cursor()

print("🏗️ Setting up normalized database...")

# Create destinations table (dimension table)
cursor.execute('''
DROP TABLE IF EXISTS monthly_stats;
''')

cursor.execute('''
DROP TABLE IF EXISTS destinations;
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    region TEXT,
    type TEXT,
    avg_satisfaction REAL
)
''')

# Create monthly_stats table (fact table)
cursor.execute('''
CREATE TABLE IF NOT EXISTS monthly_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER,
    month TEXT,
    year INTEGER,
    category TEXT,
    visitors REAL,
    avg_spend_per_visitor REAL,
    total_revenue REAL,
    satisfaction_score REAL,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
)
''')

# Load CSV data
df = pd.read_csv('indonesia_tourism_2024.csv')
print(f"📊 CSV columns: {list(df.columns)}")

# Helper function for regions
def determine_region(destination):
    regions = {
        'Bali': 'Bali',
        'Jakarta': 'Java',
        'Bandung': 'Java',
        'Yogyakarta': 'Java',
        'Surabaya': 'Java',
        'Lombok': 'NTB',
        'Komodo': 'NTT',
        'Raja Ampat': 'Papua',
        'Lake Toba': 'Sumatra',
        'Medan': 'Sumatra'
    }
    return regions.get(destination, 'Other')

# Get unique destinations and insert
destinations_dict = {}

print(f"📍 Inserting {len(df['destination'].unique())} unique destinations...")

for idx, dest_row in df.drop_duplicates('destination').iterrows():
    dest_name = dest_row['destination']
    avg_sat = df[df['destination'] == dest_name]['satisfaction_score'].mean()
    
    cursor.execute('''
        INSERT INTO destinations (name, region, type, avg_satisfaction)
        VALUES (?, ?, ?, ?)
    ''', (dest_name, determine_region(dest_name), 'Cultural', round(avg_sat, 2)))
    
    destinations_dict[dest_name] = cursor.lastrowid

# Insert monthly records
print(f"📊 Inserting {len(df)} monthly records...")

for idx, row in df.iterrows():
    dest_id = destinations_dict[row['destination']]
    cursor.execute('''
        INSERT INTO monthly_stats 
        (destination_id, month, year, category, visitors, avg_spend_per_visitor, total_revenue, satisfaction_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dest_id, row['month'], row['year'], row['category'], 
          row['visitors'], row['avg_spend_per_visitor'], 
          row['total_revenue'], row['satisfaction_score']))

# Commit and close
conn.commit()

# Verify counts
cursor.execute("SELECT COUNT(*) FROM destinations")
dest_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM monthly_stats")
stats_count = cursor.fetchone()[0]

conn.close()

print(f"✅ Database created successfully!")
print(f"   📍 Destinations table: {dest_count} records")
print(f"   📊 Monthly stats table: {stats_count} records")
print(f"   💾 Database file: tourism.db")
