import pandas as pd
from datasets import load_dataset
import os

print("Downloading dataset...")
dataset = load_dataset("cardiffnlp/tweet_eval", "sentiment")

train_df = dataset['train'].to_pandas()
val_df = dataset['validation'].to_pandas()
test_df = dataset['test'].to_pandas()

# Combine all splits for a massive dataset
df = pd.concat([train_df, val_df, test_df], ignore_index=True)

# Map labels
def map_label(label):
    if label == 0:
        return 'negative'
    elif label == 1:
        return 'neutral'
    elif label == 2:
        return 'positive'

df['sentiment'] = df['label'].apply(map_label)
# rename column
df.rename(columns={'text': 'text'}, inplace=True)
df = df[['text', 'sentiment']]

print(f"Total rows: {len(df)}")
print(df['sentiment'].value_counts())

os.makedirs('../data/raw', exist_ok=True)
df.to_csv('../data/raw/tweet_eval_sentiment.csv', index=False)
print("Saved to ../data/raw/tweet_eval_sentiment.csv")
