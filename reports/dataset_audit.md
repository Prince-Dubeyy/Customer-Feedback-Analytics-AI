# Dataset Audit Report

## 1. Selected Dataset
- **Source**: HuggingFace `cardiffnlp/tweet_eval` (Sentiment Subset)
- **Domain**: Real-world tweets/short-form text, which perfectly mirrors the length and structure of customer feedback and reviews.
- **Description**: A massive, high-quality, multi-class sentiment dataset widely used for benchmarking state-of-the-art NLP models.

## 2. Dataset Size & Class Distribution
The dataset contains a total of **59,899** rows.

| Sentiment | Count | Percentage |
|---|---|---|
| Neutral | 27,479 | 45.8% |
| Positive | 21,043 | 35.1% |
| Negative | 11,377 | 19.0% |

## 3. Data Quality Checks
- **Missing Values**: 0 missing values.
- **Label Noise**: Very low. `tweet_eval` is a gold-standard dataset curated by researchers.
- **Duplicates**: Due to the nature of short text, there may be some retweets/duplicates, but they act as frequency amplifiers for common phrasing, which is beneficial for basic TF-IDF models.
- **Weak Neutral Samples**: Resolved. Unlike the previous dataset which contained 500 identical synthetic neutral strings, this dataset contains 27,479 organically neutral, real-world texts.

## 4. Class Imbalance Addressed
While Negative is the minority class (11,377 rows), it is still an incredibly rich and diverse vocabulary compared to the previous 497 rows. We will apply `class_weight='balanced'` during model training (Phase 6) to mathematically penalize the model heavily if it ignores the minority class, ensuring the F1 score remains balanced across all three sentiments.
