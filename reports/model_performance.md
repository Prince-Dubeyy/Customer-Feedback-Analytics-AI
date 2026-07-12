# AI Model Performance Report

## Model Overview
- **Model Architecture**: Logistic Regression
- **Feature Engineering**: TF-IDF (ngram_range=(1,2), max_features=15000)
- **Dataset**: Yelp Reviews Full (Mapped to 3 classes)
- **Dataset Size**: 74996 samples
- **Classes**: Positive, Neutral, Negative

## Performance Metrics (Test Set)
- **Accuracy**: 0.7361
- **Precision (weighted)**: 0.7358
- **Recall (weighted)**: 0.7361
- **F1 Score (weighted)**: 0.7359

## Classification Report
```text
              precision    recall  f1-score   support

    negative       0.80      0.80      0.80      5000
     neutral       0.64      0.64      0.64      5000
    positive       0.77      0.77      0.77      5000

    accuracy                           0.74     15000
   macro avg       0.74      0.74      0.74     15000
weighted avg       0.74      0.74      0.74     15000

```

## Next Steps
This model achieves much higher accuracy due to the high quality dataset!
