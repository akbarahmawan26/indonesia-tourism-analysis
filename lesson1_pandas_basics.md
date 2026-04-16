# 🐍 Python + Pandas Tutorial: Tourism Data Analysis
## Lesson 1: First Steps with Real Tourism Data
### For UKP Pariwisata AI Specialist Role

---

## 🎯 What You'll Learn (30-45 minutes)

By the end of this lesson, you'll be able to:
- ✅ Read CSV files with Pandas
- ✅ Filter and clean tourism data
- ✅ Calculate basic statistics
- ✅ Create your first visualization
- ✅ Export results

---

## 📝 Step 1: Setup (5 minutes)

Open your terminal and run:

```bash
# Create a project folder
mkdir ~/ukp_ai_learning
cd ~/ukp_ai_learning

# Create a Python virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR: venv\Scripts\activate  # On Windows

# Install required packages
pip install pandas matplotlib seaborn
```

---

## 📊 Step 2: Create Sample Tourism Data (10 minutes)

We'll create realistic Indonesian tourism data to practice with:

```python
# save this as create_tourism_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data
destinations = ['Bali', 'Yogyakarta', 'Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Makassar', 'Lombok']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
categories = ['Domestic', 'International']

# Generate 200 records
data = []
for i in range(200):
    dest = np.random.choice(destinations)
    month = np.random.choice(months)
    category = np.random.choice(categories)
    
    # Generate realistic visitor numbers
    if category == 'International':
        visitors = np.random.randint(5000, 50000)
    else:
        visitors = np.random.randint(20000, 150000)
    
    # Revenue calculation
    if category == 'International':
        avg_spend = np.random.randint(2000000, 5000000)  # Rupiah
    else:
        avg_spend = np.random.randint(500000, 1500000)
    
    revenue = visitors * avg_spend
    
    # Satisfaction score (0-10)
    satisfaction = np.random.uniform(6.5, 9.5)
    
    data.append({
        'destination': dest,
        'month': month,
        'year': 2024,
        'category': category,
        'visitors': visitors,
        'avg_spend_per_visitor': avg_spend,
        'total_revenue': revenue,
        'satisfaction_score': round(satisfaction, 1)
    })

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('indonesia_tourism_2024.csv', index=False)
print(f"✅ Created {len(df)} tourism records")
print("\nFirst 5 rows:")
print(df.head())
print(f"\nSaved to: indonesia_tourism_2024.csv")
```

---

## 🔍 Step 3: Load and Explore Data (10 minutes)

Create a new file called `explore_tourism.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('indonesia_tourism_2024.csv')

print("📊 DATA OVERVIEW")
print("=" * 50)
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData Types:")
print(df.dtypes)

print("\n🔎 FIRST 10 RECORDS")
print("=" * 50)
print(df.head(10))

print("\n📈 BASIC STATISTICS")
print("=" * 50)
print(df.describe())

print("\n🌍 DESTINATIONS")
print("=" * 50)
print(df['destination'].value_counts())

print("\n👥 VISITOR CATEGORIES")
print("=" * 50)
print(df['category'].value_counts())
```

**Run it:**
```bash
python3 explore_tourism.py
```

---

## 📊 Step 4: Analyze and Filter (10 minutes)

Create `analyze_tourism.py`:

```python
import pandas as pd

# Load data
df = pd.read_csv('indonesia_tourism_2024.csv')

print("🎯 ANALYSIS: TOP PERFORMING DESTINATIONS")
print("=" * 60)

# 1. Total visitors by destination
visitors_by_dest = df.groupby('destination')['visitors'].sum().sort_values(ascending=False)
print("\n1. Total Visitors by Destination:")
print(visitors_by_dest)

# 2. International vs Domestic
print("\n\n2. Domestic vs International Visitors:")
category_stats = df.groupby('category').agg({
    'visitors': 'sum',
    'total_revenue': 'sum',
    'satisfaction_score': 'mean'
})
print(category_stats)

# 3. Best performing months
print("\n\n3. Monthly Visitor Trends:")
monthly_visitors = df.groupby('month')['visitors'].sum()
# Reorder by calendar
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_visitors = monthly_visitors.reindex(month_order)
print(monthly_visitors)

# 4. High satisfaction destinations (>8.5)
print("\n\n4. High Satisfaction Destinations (>8.5):")
high_sat = df[df['satisfaction_score'] > 8.5]
high_sat_summary = high_sat.groupby('destination')['visitors'].sum().sort_values(ascending=False)
print(high_sat_summary)

# 5. Bali analysis (most popular)
print("\n\n5. BALI DETAILED ANALYSIS:")
bali_data = df[df['destination'] == 'Bali']
bali_summary = bali_data.groupby('category').agg({
    'visitors': 'sum',
    'total_revenue': 'sum',
    'satisfaction_score': 'mean'
})
print(bali_summary)
```

---

## 📈 Step 5: Create Visualizations (10 minutes)

Create `visualize_tourism.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
df = pd.read_csv('indonesia_tourism_2024.csv')

# Create 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Visitors by Destination (Bar Chart)
visitors_by_dest = df.groupby('destination')['visitors'].sum().sort_values(ascending=True)
visitors_by_dest.plot(kind='barh', ax=axes[0,0], color='steelblue')
axes[0,0].set_title('Total Visitors by Destination', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Total Visitors')

# 2. Category Pie Chart
category_data = df.groupby('category')['visitors'].sum()
axes[0,1].pie(category_data, labels=category_data.index, autopct='%1.1f%%', 
              colors=['lightcoral', 'skyblue'])
axes[0,1].set_title('Domestic vs International Visitors', fontsize=14, fontweight='bold')

# 3. Monthly Trend (Line Chart)
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_visitors = df.groupby('month')['visitors'].sum().reindex(month_order)
axes[1,0].plot(monthly_visitors.index, monthly_visitors.values, marker='o', linewidth=2, color='green')
axes[1,0].set_title('Monthly Visitor Trends', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Month')
axes[1,0].set_ylabel('Total Visitors')
axes[1,0].tick_params(axis='x', rotation=45)

# 4. Satisfaction vs Revenue Scatter
for dest in df['destination'].unique():
    dest_data = df[df['destination'] == dest]
    axes[1,1].scatter(dest_data['satisfaction_score'], dest_data['total_revenue']/1e9, 
                      label=dest, s=60, alpha=0.7)
axes[1,1].set_title('Satisfaction vs Revenue', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Satisfaction Score')
axes[1,1].set_ylabel('Revenue (Billion Rupiah)')
axes[1,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('tourism_analysis.png', dpi=150, bbox_inches='tight')
print("✅ Saved visualization to: tourism_analysis.png")
plt.show()
```

---

## ✅ Your First Deliverable

After completing this lesson, you'll have:
1. ✅ `indonesia_tourism_2024.csv` — Realistic tourism dataset
2. ✅ `explore_tourism.py` — Data exploration script
3. ✅ `analyze_tourism.py` — Analysis script
4. ✅ `visualize_tourism.py` — Visualization script
5. ✅ `tourism_analysis.png` — Professional charts
6. ✅ Pandas fundamentals mastered

---

## 🚀 Next Steps

**Before moving to Lesson 2, you should be able to:**
- Load CSV files with `pd.read_csv()`
- View data with `.head()`, `.describe()`
- Filter with `df[df['column'] > value]`
- Group and aggregate with `.groupby()`
- Create basic visualizations

**Lesson 2 Preview:** SQL + Python Integration (store this data in a real database!)

---

## ❓ Stuck?

If you get errors, check:
1. Are you in the virtual environment? (venv activated)
2. Did you install pandas? `pip install pandas matplotlib seaborn`
3. Is the CSV file in the same folder as your scripts?

**Type your errors here and I'll help! 🙋**
