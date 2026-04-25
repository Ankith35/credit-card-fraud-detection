import pandas as pd


# 1. LOAD THE DATA
df = pd.read_csv('creditcard.csv.csv')

# 2. IDENTIFY THE COLUMNS
target_col = 'is_fraud'
# Usually, the transaction amount in this file is 'amt'
amt_col = 'amt'

# 3. THE CALCULATION
total_transactions = len(df)
fraud_cases = df[df[target_col] == 1]
num_fraud = len(fraud_cases)
fraud_percentage = (num_fraud / total_transactions) * 100

# 4. REVENUE AT RISK
# We calculate how much money was actually stolen
total_stolen = fraud_cases[amt_col].sum()

print(f"--- FINTECH AUDIT REPORT ---")
print(f"Total Transactions Scanned: {total_transactions:,}")
print(f"Fraudulent Hits: {num_fraud}")
print(f"Fraud Percentage: {fraud_percentage:.4f}%")
print(f"TOTAL REVENUE LOST TO FRAUD: ₹{total_stolen:,.2f}")

# 5. THE "WHO IS BEING TARGETED?" INSIGHT
# Let's see if fraud happens to older or younger people (using 'dob' column)
print(f"\n--- ATTACK PATTERN ---")
print(f"Average Fraud Transaction Amount: ₹{fraud_cases[amt_col].mean():.2f}")
print(f"Max Fraud Amount   : ₹{fraud_cases['amt'].max():,.2f}")

# 1. Find the top 5 jobs most targeted by fraud
top_fraud_jobs = fraud_cases['job'].value_counts().head(5)

print("--- TOP 5 TARGETED PROFESSIONS ---")
print(top_fraud_jobs)

# 2. Find the top 5 cities where fraud is happening
top_fraud_cities = fraud_cases['city'].value_counts().head(5)

print("\n--- TOP 5 FRAUD HOTSPOTS (CITIES) ---")
print(top_fraud_cities)

import seaborn as sns
import matplotlib.pyplot as plt

# Let's visualize the Top 5 Cities
plt.figure(figsize=(5,3))
sns.barplot(x=top_fraud_cities.index, y=top_fraud_cities.values, palette='Reds_r')

plt.title('CRIME HOTSPOTS: Top 5 Cities by Fraud Count', fontsize=15)
plt.xlabel('City Name', fontsize=12)
plt.ylabel('Number of Fraud Cases', fontsize=12)
plt.show()

top_fraud_jobs = fraud_cases['job'].value_counts().head(10)
print(top_fraud_jobs)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(21,9))
sns.barplot(x=top_fraud_jobs.index, y=top_fraud_jobs.values, palette='Purples_r')

plt.title('Crime Hotspots : Top 10 jobs by fraud count',fontsize=15)
plt.xlabel('job',fontsize=12)
plt.ylabel('number of fraud cases',fontsize=12)
plt.show()

#---Clean & Engineer Features---

import numpy as np
from datetime import datetime

print(df.columns.tolist())
print(df[['trans_date_trans_time', 'is_fraud']].head())

# Parse datetime - with error handling
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'], errors='coerce')
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')  # errors='coerce' handles bad dates

# Feature engineering
df['hour'] = df['trans_date_trans_time'].dt.hour
df['day_of_week'] = df['trans_date_trans_time'].dt.day_name()
df['month'] = df['trans_date_trans_time'].dt.month_name()
df['age'] = ((df['trans_date_trans_time'] - df['dob']).dt.days // 365)
df['age_group'] = pd.cut(df['age'], bins=[0,25,35,45,55,65,100],
                          labels=['<25','25-35','35-45','45-55','55-65','65+'])

print("Nulls:", df.isnull().sum().sum())
print("Shape:", df.shape)

#---Audit Report---
total = len(df)
fraud = df[df['is_fraud'] == 1]
num_fraud = len(fraud)

print("--- FINTECH AUDIT REPORT ---")
print(f"Total Transactions : {total:,}")
print(f"Fraudulent Hits    : {num_fraud:,}")
print(f"Fraud Rate         : {num_fraud/total*100:.4f}%")
print(f"Total Stolen       : ₹{fraud['amt'].sum():,.2f}")
print(f"Avg Fraud Amount   : ₹{fraud['amt'].mean():,.2f}")
print(f"Max Fraud Amount   : ₹{fraud['amt'].max():,.2f}")

#--Fraud by Hour of Day--

hourly = df.groupby(['hour','is_fraud']).size().unstack(fill_value=0)

# Rename columns clearly
hourly.columns = ['legit', 'fraud']
hourly['fraud_rate'] = hourly['fraud'] / (hourly['legit'] + hourly['fraud']) * 100

plt.figure(figsize=(14,4))
plt.plot(hourly.index, hourly['fraud_rate'], color='crimson', marker='o')
plt.title('Fraud Rate by Hour of Day', fontsize=15)
plt.xlabel('Hour (0-23)')
plt.ylabel('Fraud Rate (%)')
plt.xticks(range(0,24))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fraud_by_hour.png', dpi=150)
plt.show()

#---Fraud by Day of Week---

order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_fraud = fraud['day_of_week'].value_counts().reindex(order)

plt.figure(figsize=(10,4))
sns.barplot(x=day_fraud.index, y=day_fraud.values, palette='OrRd_r')
plt.title('Fraud Cases by Day of Week', fontsize=15)
plt.xlabel('Day')
plt.ylabel('Fraud Cases')
plt.tight_layout()
plt.savefig('fraud_by_day.png', dpi=150)
plt.show()

#---Fraud by Merchant Category---

cat_fraud = fraud['category'].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(x=cat_fraud.values, y=cat_fraud.index, palette='Reds_r')
plt.title('Top 10 Merchant Categories by Fraud Count', fontsize=15)
plt.xlabel('Fraud Cases')
plt.tight_layout()
plt.savefig('fraud_by_category.png', dpi=150)
plt.show()

#---Fraud by Age Group---

age_fraud = fraud['age_group'].value_counts().sort_index()

plt.figure(figsize=(9,4))
sns.barplot(x=age_fraud.index, y=age_fraud.values, palette='magma')
plt.title('Fraud Cases by Age Group', fontsize=15)
plt.xlabel('Age Group')
plt.ylabel('Fraud Cases')
plt.tight_layout()
plt.savefig('fraud_by_age.png', dpi=150)
plt.show()

#---Fraud by Gender---

gender_stats = df.groupby('gender')['is_fraud'].agg(['sum','count'])
gender_stats['fraud_rate'] = gender_stats['sum'] / gender_stats['count'] * 100
print(gender_stats)

plt.figure(figsize=(5,4))
sns.barplot(x=gender_stats.index, y=gender_stats['fraud_rate'], palette=['PINK','SKYBLUE'])
plt.title('Fraud Rate by Gender', fontsize=14)
plt.ylabel('Fraud Rate (%)')
plt.tight_layout()
plt.savefig('fraud_by_gender.png', dpi=150)
plt.show()

#---Transaction Amount Distribution---

plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
df[df['is_fraud']==0]['amt'].clip(upper=1000).hist(bins=50, color='steelblue', edgecolor='white')
plt.title('Legitimate Transaction Amounts')
plt.xlabel('Amount (₹)')

plt.subplot(1,2,2)
df[df['is_fraud']==1]['amt'].clip(upper=1000).hist(bins=50, color='crimson', edgecolor='white')
plt.title('Fraud Transaction Amounts')
plt.xlabel('Amount (₹)')

plt.tight_layout()
plt.savefig('amount_distribution.png', dpi=150)
plt.show()

#---Correlation Heatmap---

num_cols = ['amt','hour','age','is_fraud']
corr = df[num_cols].corr()

plt.figure(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap', fontsize=14)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150)
plt.show()

#---State-level Fraud Summary---
state_fraud = df.groupby('state').agg(
    total=('is_fraud','count'),
    fraud_cases=('is_fraud','sum'),
    total_stolen=('amt', lambda x: x[df.loc[x.index,'is_fraud']==1].sum())
).reset_index()
state_fraud['fraud_rate'] = state_fraud['fraud_cases'] / state_fraud['total'] * 100
state_fraud.sort_values('fraud_cases', ascending=False).head(10)

# --- Export to MySQL ---
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus('ankithh@1356')
engine = create_engine(f'mysql+pymysql://root:{password}@127.0.0.1/fraud_detection')

df.to_sql('transactions', con=engine, if_exists='replace', 
          index=True, index_label='id', chunksize=1000)

print("✅ Done! Rows inserted:", len(df))

