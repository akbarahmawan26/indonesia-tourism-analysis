import pandas as pd

# Load data
df = pd.read_csv('indonesia_tourism_2024.csv')

print("🎯 TOURISM ANALYSIS: INSIGHTS FOR UKP PARIWISATA")
print("=" * 60)

# 1. Total visitors by destination
print("\n1. 📊 Total Visitors by Destination:")
print("-" * 40)
visitors_by_dest = df.groupby('destination')['visitors'].sum().sort_values(ascending=False)
for dest, visitors in visitors_by_dest.items():
    print(f"   {dest:12} {visitors:>12,} visitors")

# 2. Revenue analysis
print("\n\n2. 💰 Revenue by Destination (Billion Rupiah):")
print("-" * 40)
revenue_by_dest = df.groupby('destination')['total_revenue'].sum().sort_values(ascending=False) / 1e9
for dest, revenue in revenue_by_dest.items():
    print(f"   {dest:12} {revenue:>10.1f} Billion IDR")

# 3. International vs Domestic
print("\n\n3. 🌏 Domestic vs International Visitors:")
print("-" * 40)
category_stats = df.groupby('category').agg({
    'visitors': 'sum',
    'total_revenue': 'sum',
    'satisfaction_score': 'mean'
})
category_stats['total_revenue'] = category_stats['total_revenue'] / 1e9
print(category_stats)

# 4. Average satisfaction score
print("\n\n4. 😊 Average Satisfaction by Destination:")
print("-" * 40)
satisfaction_by_dest = df.groupby('destination')['satisfaction_score'].mean().sort_values(ascending=False)
for dest, score in satisfaction_by_dest.items():
    stars = '⭐' * int(score)
    print(f"   {dest:12} {score:.1f} {stars}")

# 5. Best performing months
print("\n\n5. 📅 Peak Tourism Months:")
print("-" * 40)
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_visitors = df.groupby('month')['visitors'].sum().reindex(month_order)
top_3_months = monthly_visitors.nlargest(3)
for month, visitors in top_3_months.items():
    print(f"   {month:3} {visitors:>12,} visitors")

# 6. Bali insight (since it's the most popular)
print("\n\n6. 🏝️  BALI DETAILED BREAKDOWN:")
print("-" * 40)
bali_data = df[df['destination'] == 'Bali']
bali_summary = bali_data.groupby('category').agg({
    'visitors': 'sum',
    'total_revenue': 'sum',
    'satisfaction_score': 'mean'
})
bali_summary['total_revenue'] = bali_summary['total_revenue'] / 1e9
print(bali_summary)

# 7. High satisfaction destinations
print("\n\n7. ⭐ Top Satisfaction Destinations (>8.5/10):")
print("-" * 40)
high_satisfaction = df[df['satisfaction_score'] > 8.5]
top_satisfaction = high_satisfaction.groupby('destination')['visitors'].sum().sort_values(ascending=False)
for dest, visitors in top_satisfaction.items():
    avg_score = high_satisfaction[high_satisfaction['destination'] == dest]['satisfaction_score'].mean()
    print(f"   {dest:12} {visitors:>10,} visitors (Score: {avg_score:.1f})")

print("\n" + "=" * 60)
print("✅ Analysis Complete! Ready for visualization...")
