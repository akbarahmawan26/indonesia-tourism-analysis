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
