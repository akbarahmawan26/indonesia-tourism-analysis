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
fig.suptitle('Indonesia Tourism Analysis 2024 - UKP Pariwisata Dashboard', 
             fontsize=16, fontweight='bold')

# 1. Visitors by Destination (Bar Chart)
visitors_by_dest = df.groupby('destination')['visitors'].sum().sort_values(ascending=True)
visitors_by_dest.plot(kind='barh', ax=axes[0,0], color='steelblue')
axes[0,0].set_title('Total Visitors by Destination', fontsize=12, fontweight='bold')
axes[0,0].set_xlabel('Total Visitors')
for i, v in enumerate(visitors_by_dest.values):
    axes[0,0].text(v + 1000, i, f'{v:,}', va='center', fontsize=9)

# 2. Category Pie Chart
category_data = df.groupby('category')['visitors'].sum()
colors = ['#ff9999', '#66b3ff']
axes[0,1].pie(category_data, labels=category_data.index, autopct='%1.1f%%', 
              colors=colors, startangle=90)
axes[0,1].set_title('Visitor Distribution', fontsize=12, fontweight='bold')

# 3. Monthly Trend (Line Chart)
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_visitors = df.groupby('month')['visitors'].sum().reindex(month_order)
axes[1,0].plot(monthly_visitors.index, monthly_visitors.values, 
               marker='o', linewidth=2, color='green', markersize=8)
axes[1,0].set_title('Monthly Visitor Trends', fontsize=12, fontweight='bold')
axes[1,0].set_xlabel('Month')
axes[1,0].set_ylabel('Total Visitors')
axes[1,0].tick_params(axis='x', rotation=45)
axes[1,0].grid(True, alpha=0.3)

# 4. Revenue vs Satisfaction Scatter
for dest in df['destination'].unique():
    dest_data = df[df['destination'] == dest]
    revenue_billions = dest_data['total_revenue'] / 1e9
    axes[1,1].scatter(dest_data['satisfaction_score'], revenue_billions, 
                      label=dest, s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[1,1].set_title('Satisfaction vs Revenue', fontsize=12, fontweight='bold')
axes[1,1].set_xlabel('Satisfaction Score (0-10)')
axes[1,1].set_ylabel('Revenue (Billion Rupiah)')
axes[1,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for title
plt.savefig('tourism_analysis.png', dpi=150, bbox_inches='tight')
print("✅ Saved visualization to: tourism_analysis.png")
print("\nOpen 'tourism_analysis.png' to see your visualizations!")
plt.show()
