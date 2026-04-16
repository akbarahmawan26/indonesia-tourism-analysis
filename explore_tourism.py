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
