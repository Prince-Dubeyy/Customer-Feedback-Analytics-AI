# %% [markdown]
# # Exploratory Data Analysis
# Analyze sentiment distribution, review lengths, and frequent words.

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

# %%
df = pd.read_csv('../data/processed/preprocessed_reviews.csv')
os.makedirs('../reports/figures', exist_ok=True)

# %%
# Sentiment Distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='sentiment', order=['positive', 'negative'])
plt.title('Sentiment Distribution')
plt.savefig('../reports/figures/sentiment_distribution.png')
plt.close()

# %%
# Review Length Distribution
df['review_length'] = df['processed_text'].astype(str).apply(len)
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='review_length', bins=50, kde=True)
plt.title('Review Length Distribution')
plt.savefig('../reports/figures/review_length.png')
plt.close()

# %%
# Most frequent words for each sentiment
def plot_top_words(sentiment, color):
    text = " ".join(df[df['sentiment'] == sentiment]['processed_text'].astype(str))
    word_counts = Counter(text.split())
    common_words = pd.DataFrame(word_counts.most_common(20), columns=['Word', 'Count'])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=common_words, x='Count', y='Word', color=color)
    plt.title(f'Top 20 Words in {sentiment.capitalize()} Reviews')
    plt.savefig(f'../reports/figures/top_words_{sentiment}.png')
    plt.close()

plot_top_words('positive', 'green')
plot_top_words('negative', 'red')
print("Figures saved to ../reports/figures/")
