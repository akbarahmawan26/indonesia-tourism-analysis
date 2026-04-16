"""
Lesson 2: SQL Practice with Tourism Data
Practice SQL queries on the normalized database
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('tourism.db')
cursor = conn.cursor()

print("=" * 60)
print("🎯 SQL PRACTICE: Indonesia Tourism Analytics")
print("=" * 60)

# Query 1: Top destinations by total visitors
print("\n1️⃣ Top 5 destinations by total visitors:")
cursor.execute('''
    SELECT d.name, d.region, SUM(m.visitors) as total_visitors
    FROM destinations d
    JOIN monthly_stats m ON d.id = m.destination_id
    GROUP BY d.name, d.region
    ORDER BY total_visitors DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}): {row[2]:,.0f} visitors")

# Query 2: Domestic vs International visitors
print("\n2️⃣ Domestic vs International visitors:")
cursor.execute('''
    SELECT m.category, SUM(m.visitors) as total_visitors,
           ROUND(AVG(m.satisfaction_score), 2) as avg_sat
    FROM monthly_stats m
    GROUP BY m.category
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]:,.0f} visitors (Avg satisfaction: {row[2]})")

# Query 3: Monthly trends (peak season analysis)
print("\n3️⃣ Monthly visitation trends:")
cursor.execute('''
    SELECT m.month, SUM(m.visitors) as total_visitors
    FROM monthly_stats m
    GROUP BY m.month
    ORDER BY CASE m.month
        WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
        WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
        WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
        WHEN 'October' THEN 10 WHEN 'November' THEN 11 ELSE 12
    END
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]:,.0f} visitors")

# Query 4: High-revenue destinations
print("\n4️⃣ Top revenue-generating destinations:")
cursor.execute('''
    SELECT d.name, d.region,
           ROUND(SUM(m.total_revenue)/1e12, 2) as revenue_trillion_idr
    FROM destinations d
    JOIN monthly_stats m ON d.id = m.destination_id
    GROUP BY d.name, d.region
    ORDER BY revenue_trillion_idr DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}): {row[2]}T IDR")

# Query 5: Regions comparison
print("\n5️⃣ Performance by region:")
cursor.execute('''
    SELECT d.region,
           COUNT(DISTINCT d.name) as num_destinations,
           ROUND(SUM(m.total_revenue)/1e12, 2) as total_revenue_trillion,
           ROUND(AVG(m.satisfaction_score), 2) as avg_satisfaction
    FROM destinations d
    JOIN monthly_stats m ON d.id = m.destination_id
    GROUP BY d.region
    ORDER BY total_revenue_trillion DESC
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} destinations, {row[2]}T IDR revenue, Avg sat: {row[3]}")

# Query 6: Satisfaction leaders
print("\n6️⃣ Top satisfaction destinations:")
cursor.execute('''
    SELECT d.name, ROUND(AVG(m.satisfaction_score), 2) as avg_satisfaction,
           ROUND(AVG(m.visitors), 0) as avg_monthly_visitors
    FROM destinations d
    JOIN monthly_stats m ON d.id = m.destination_id
    GROUP BY d.name
    HAVING COUNT(*) >= 3
    ORDER BY avg_satisfaction DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]}/5.0 ({row[2]:,.0f} avg monthly visitors)")

# Query 7: Most efficient destinations (revenue per visitor)
print("\n7️⃣ Revenue efficiency analysis:")
cursor.execute('''
    SELECT d.name,
           ROUND(SUM(m.total_revenue)/SUM(m.visitors)/1e6, 2) as revenue_per_visitor_millions
    FROM destinations d
    JOIN monthly_stats m ON d.id = m.destination_id
    GROUP BY d.name
    ORDER BY revenue_per_visitor_millions DESC
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]}M IDR per visitor")

# Query 8: Year-over-year comparison
print("\n8️⃣ Year comparison:")
cursor.execute('''
    SELECT m.year, SUM(m.visitors) as total_visitors,
           ROUND(SUM(m.total_revenue)/1e12, 2) as total_revenue_trillion,
           ROUND(AVG(m.satisfaction_score), 2) as avg_satisfaction
    FROM monthly_stats m
    GROUP BY m.year
    ORDER BY m.year
''')
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]:,.0f} visitors, {row[2]}T IDR revenue, Avg sat: {row[3]}")

print("\n" + "=" * 60)
print("✅ Analysis complete! Practice SQL skills acquired.")
print("=" * 60)

conn.close()
