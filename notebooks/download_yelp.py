import pandas as pd
from datasets import load_dataset
import os

print("Downloading Yelp dataset...")
dataset = load_dataset("yelp_review_full")

train_df = dataset['train'].to_pandas()

# Map stars (0-4 in dataset, corresponding to 1-5 stars)
# 0, 1 -> negative (1-2 stars)
# 2 -> neutral (3 stars)
# 3, 4 -> positive (4-5 stars)

def map_label(label):
    if label in [0, 1]:
        return 'negative'
    elif label == 2:
        return 'neutral'
    elif label in [3, 4]:
        return 'positive'

train_df['sentiment'] = train_df['label'].apply(map_label)
train_df = train_df[['text', 'sentiment']]

# Create a balanced dataset of 60,000 rows (20,000 per class)
df_negative = train_df[train_df['sentiment'] == 'negative'].sample(20000, random_state=42)
df_neutral = train_df[train_df['sentiment'] == 'neutral'].sample(20000, random_state=42)
df_positive = train_df[train_df['sentiment'] == 'positive'].sample(20000, random_state=42)

df = pd.concat([df_negative, df_neutral, df_positive], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Total rows: {len(df)}")
print(df['sentiment'].value_counts())

os.makedirs('../data/raw', exist_ok=True)
df.to_csv('../data/raw/yelp_sentiment.csv', index=False)
print("Saved to ../data/raw/yelp_sentiment.csv")
