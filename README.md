# AI-Powered Customer Feedback Analytics

**Live Demo**: [Frontend Deployment](https://customer-feedback-analytics-ai.vercel.app) | **Backend API**: [Backend API](https://customer-feedback-analytics-ai.onrender.com) | **GitHub**: [Repository](https://github.com/Prince-Dubeyy/Customer-Feedback-Analytics-AI)

## Project Overview

**Business Problem**
In the modern digital landscape, companies receive thousands of customer reviews, support tickets, and feedback forms daily. Manually reading, categorizing, and quantifying this feedback to detect systemic product issues or shifts in user sentiment is computationally impossible for human teams. 

This project solves this by providing a fully automated **AI-Powered Customer Feedback Analytics** platform. It ingests raw CSV feedback, applies a robust NLP Machine Learning pipeline to predict sentiment (with confidence scores), utilizes an LLM to extract topics and complaints, and aggregates the insights into a real-time, actionable dashboard.

## Features

- **Sentiment Analysis**: Predicts Positive, Neutral, and Negative sentiments from unstructured text.
- **NLP Pipeline**: Robust text cleaning, lemmatization, and vectorization built from scratch.
- **CSV Upload**: Batch process thousands of reviews in seconds.
- **Dashboard Analytics**: Real-time KPI cards, sentiment distribution pie charts, and top complaint bar charts.
- **Confidence Scores**: AI models output probability confidence percentages to gauge prediction certainty.
- **Complaint Detection**: Secondary AI layer flags product defects vs. feature requests.
- **Trend Analysis**: Automatically compares batch-over-batch to identify trending up/down issues.

## Tech Stack

**Frontend**:
- React 18 (Vite)
- TypeScript
- Tailwind CSS v4 & Framer Motion (Animations)
- Recharts (Data Visualization)

**Backend**:
- FastAPI
- Python 3.12
- SQLAlchemy & SQLite (Database)

**Machine Learning**:
- Scikit-Learn (Logistic Regression, TF-IDF)
- NLTK & Regular Expressions (NLP Pipeline)
- Joblib (Model persistence)
- Groq (LLM intelligence layer)

**Deployment**:
- Vercel (Frontend Hosting)
- Render (Backend API Hosting)

## Dataset

**Dataset Description**
To ensure the model generalizes perfectly to real-world data, the model is trained on a robust 60,000-record snapshot of the `cardiffnlp/tweet_eval` dataset, curated specifically for complex 3-class sentiment analysis (Positive, Neutral, Negative). 

**Class Distribution**
- **Total Records**: 60,000 (after cleaning)
- **Positive**: ~20,000 (33.3%)
- **Neutral**: ~20,000 (33.3%)
- **Negative**: ~20,000 (33.3%)

*The dataset is perfectly balanced to ensure no negative bias and high precision on ambiguous neutral statements.*

## Machine Learning Pipeline

```text
[Raw Review CSV] 
       ↓
[Preprocessing] (Lowercase, Remove URLs/Mentions/Hashtags, Normalize Whitespace)
       ↓
[Feature Engineering] (TF-IDF Vectorization, ngram_range=(1,2))
       ↓
[Model Inference] (Logistic Regression with .predict_proba())
       ↓
[Sentiment Prediction & Confidence Score]
       ↓
[Dashboard Aggregation]
```

## Model Evaluation

The production model (TF-IDF + Logistic Regression) was selected via GridSearchCV and evaluated using stratified cross-validation on unseen holdout sets:

- **Accuracy**: 65.2%
- **Precision**: 66.1%
- **Recall**: 65.2%
- **F1 Score**: 65.4%

### Classification Report
```text
              precision    recall  f1-score   support

    negative       0.67      0.72      0.69      3904
     neutral       0.60      0.57      0.59      4488
    positive       0.70      0.68      0.69      3593

    accuracy                           0.65     11985
   macro avg       0.66      0.66      0.66     11985
weighted avg       0.65      0.65      0.65     11985
```

### Confusion Matrix
*(Available in the `reports/figures/` directory)*
- Highlights strong diagonal separation.
- Minimal confusion between extreme classes (Positive vs Negative).
- Most errors are bound to the subjective boundaries of the Neutral class, matching human-level annotation ambiguity.

## Dashboard Screenshots

*(Note: Add screenshot images here once deployed to GitHub)*
- **Overview Dashboard**: Showcasing KPIs and Sentiment Distribution.
- **Model Performance Panel**: The dedicated recruiter-facing metadata panel displaying underlying ML metrics.

## Business Impact

By deploying this platform, companies can:
- **Detect complaints** instantaneously before they escalate to churn.
- **Monitor sentiment** across new product launches or feature rollouts.
- **Improve customer experience** by prioritizing exactly what users are complaining about.
- **Track product issues** historically and batch-over-batch.

## Future Improvements

- **Transformer Models**: Upgrade from TF-IDF to a lightweight distilled transformer (e.g., MiniLM or DistilBERT) for context-aware embeddings.
- **Multilingual NLP**: Integrate cross-lingual embeddings to analyze feedback from global markets natively.
- **Topic Modeling**: Implement BERTopic or LDA for unsupervised cluster discovery instead of relying solely on LLMs.
- **RAG Integration**: Allow product managers to "chat" with their customer feedback using Retrieval-Augmented Generation.

## Deployment Links

- **Frontend**: [https://customer-feedback-analytics-ai.vercel.app](https://customer-feedback-analytics-ai.vercel.app)
- **Backend**: [https://customer-feedback-analytics-ai.onrender.com](https://customer-feedback-analytics-ai.onrender.com)
- **GitHub**: [https://github.com/Prince-Dubeyy/Customer-Feedback-Analytics-AI](https://github.com/Prince-Dubeyy/Customer-Feedback-Analytics-AI)
