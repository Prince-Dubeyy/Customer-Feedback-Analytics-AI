# %% [markdown]
# # Model Training & Evaluation
# Train Logistic Regression on TF-IDF features and evaluate performance.

# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Load Data
df = pd.read_csv('../data/processed/preprocessed_reviews.csv')
df.dropna(subset=['processed_text', 'sentiment'], inplace=True)

# %%
# Train-Test Split
X = df['processed_text']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples")

# %%
# TF-IDF Vectorization
print("Extracting features...")
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# %%
# Model Training
print("Training Logistic Regression...")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vec, y_train)

# %%
# Evaluation
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')

with open('../reports/model_evaluation.md', 'w') as f:
    f.write("# Model Evaluation Report\n\n")
    f.write(f"- **Accuracy**: {accuracy:.4f}\n")
    f.write(f"- **Precision (weighted)**: {precision:.4f}\n")
    f.write(f"- **Recall (weighted)**: {recall:.4f}\n")
    f.write(f"- **F1 Score (weighted)**: {f1:.4f}\n\n")
    f.write("## Classification Report\n")
    f.write("```\n")
    f.write(classification_report(y_test, y_pred))
    f.write("\n```\n")

# %%
# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=['negative', 'positive'])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=['negative', 'positive'], yticklabels=['negative', 'positive'], cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('../reports/figures/confusion_matrix.png')
plt.close()

# %%
# Save artifacts
os.makedirs('../models', exist_ok=True)
joblib.dump(vectorizer, '../models/tfidf_vectorizer.joblib')
joblib.dump(model, '../models/sentiment_model.joblib')
print("Model and vectorizer saved to ../models/")
