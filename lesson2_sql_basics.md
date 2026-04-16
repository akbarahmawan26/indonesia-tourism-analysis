# Lesson 2: SQL Fundamentals for Tourism Data Analysis

## Learning Objectives
By the end of this lesson, you will:
- ✅ Understand SQL basics: SELECT, WHERE, ORDER BY, LIMIT
- ✅ Perform aggregations: COUNT, SUM, AVG, MAX, MIN, GROUP BY
- ✅ Create tables and insert data
- ✅ Join tables with JOIN operations
- ✅ Connect Python to SQLite databases
- ✅ Write complex analytical queries

## Why SQL for AI/ML?
SQL is THE language of data. As an AI Specialist:
- **80% of data** lives in databases (not CSV files!)
- **Production ML** reads from SQL databases
- **Interviews** ALWAYS include SQL questions
- **Real-world:** UKP Pariwisata likely has databases you'll query

---

## Part 1: Setting Up SQLite

SQLite is perfect for learning - no server needed, just a file!

```python
import sqlite3

# Create/connect to database
conn = sqlite3.connect('tourism.db')
cursor = conn.cursor()

# Always close when done
conn.close()
```

---

## Part 2: Creating Tables

```sql
CREATE TABLE destinations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT,
    type TEXT,
    avg_rating REAL
);

CREATE TABLE visitors (
    id INTEGER PRIMARY KEY,
    destination_id INTEGER,
    month TEXT,
    year INTEGER,
    visitor_count INTEGER,
    revenue_billion REAL,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
);
```

---

## Part 3: Essential SQL Commands

### SELECT - Retrieve Data
```sql
-- Get all columns
SELECT * FROM destinations;

-- Get specific columns
SELECT name, region FROM destinations;

-- Alias columns
SELECT name AS destination_name, region AS island FROM destinations;
```

### WHERE - Filter Data
```sql
-- Equal
SELECT * FROM destinations WHERE region = 'Bali';

-- Comparison operators
SELECT * FROM visitors WHERE revenue_billion > 2.0;

-- Multiple conditions
SELECT * FROM visitors 
WHERE month = 'March' AND revenue_billion > 1.5;

-- Pattern matching
SELECT * FROM destinations WHERE name LIKE '%Bali%';
```

### ORDER BY - Sort Results
```sql
-- Ascending (default)
SELECT * FROM visitors ORDER BY revenue_billion;

-- Descending
SELECT * FROM visitors ORDER BY revenue_billion DESC;

-- Multiple columns
SELECT * FROM visitors ORDER BY month, revenue_billion DESC;
```

### LIMIT - Top N Results
```sql
-- Top 5 destinations by revenue
SELECT * FROM visitors 
ORDER BY revenue_billion DESC 
LIMIT 5;
```

---

## Part 4: Aggregations

```sql
-- Count total records
SELECT COUNT(*) FROM visitors;

-- Sum, Average, Max, Min
SELECT 
    SUM(visitor_count) AS total_visitors,
    AVG(revenue_billion) AS avg_revenue,
    MAX(revenue_billion) AS max_revenue,
    MIN(revenue_billion) AS min_revenue
FROM visitors;

-- Group by destination
SELECT 
    d.name,
    SUM(v.revenue_billion) AS total_revenue,
    AVG(v.visitor_count) AS avg_visitors
FROM visitors v
JOIN destinations d ON v.destination_id = d.id
GROUP BY d.id, d.name
ORDER BY total_revenue DESC;
```

---

## Part 5: Joins - Connect Tables

```sql
-- INNER JOIN - matching records only
SELECT 
    d.name AS destination,
    d.region,
    v.month,
    v.visitor_count,
    v.revenue_billion
FROM destinations d
INNER JOIN visitors v ON d.id = v.destination_id;

-- LEFT JOIN - all from left table
SELECT 
    d.name,
    COALESCE(SUM(v.revenue_billion), 0) AS total_revenue
FROM destinations d
LEFT JOIN visitors v ON d.id = v.destination_id
GROUP BY d.id, d.name;
```

---

## Part 6: Python + SQL Integration

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('tourism.db')

# Method 1: Execute SQL directly
cursor = conn.cursor()
cursor.execute("SELECT * FROM destinations WHERE region = 'Bali'")
results = cursor.fetchall()

# Method 2: Use pandas (RECOMMENDED!)
df = pd.read_sql_query("""
    SELECT d.name, v.month, v.revenue_billion
    FROM destinations d
    JOIN visitors v ON d.id = v.destination_id
    WHERE v.revenue_billion > 1.0
    ORDER BY v.revenue_billion DESC
""", conn)

conn.close()
```

---

## Part 7: Advanced Queries for Tourism Analysis

### Monthly Trends
```sql
SELECT 
    month,
    SUM(visitor_count) AS total_visitors,
    SUM(revenue_billion) AS total_revenue
FROM visitors
GROUP BY month
ORDER BY 
    CASE month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
        -- ... etc
    END;
```

### Performance by Destination Type
```sql
SELECT 
    d.type,
    COUNT(DISTINCT d.id) AS num_destinations,
    AVG(v.satisfaction_score) AS avg_satisfaction,
    SUM(v.revenue_billion) AS total_revenue
FROM destinations d
JOIN visitor_stats v ON d.id = v.destination_id
GROUP BY d.type;
```

---

## Practice Exercises

1. **Query:** Find the top 3 destinations by total revenue
2. **Query:** Calculate average satisfaction score by region
3. **Query:** Find months where visitor count exceeded 1 million
4. **Challenge:** Create a query showing revenue growth month-over-month

---

## Summary
- ✅ SQL is essential for AI/ML roles
- ✅ Use pandas `read_sql_query()` for seamless integration
- ✅ Master JOINs - they're interview favorites!
- ✅ Aggregations (GROUP BY) are crucial for reporting

**Next:** Lesson 3 - Advanced SQL + Data Engineering pipelines
