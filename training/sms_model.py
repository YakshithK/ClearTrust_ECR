import pandas as pd
import joblib
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(r'data\sms.csv')
df = df[['label', 'text']]
df.dropna(subset=['label', 'text'], inplace=True)

# Keep only ASCII characters
def is_clean_text(text):
    return bool(re.match(r'^[\x00-\x7F]+$', text))

df = df[df['text'].apply(is_clean_text)]

# Count samples of each class
class_counts = df['label'].value_counts()
plt.figure(figsize=(6, 4))
plt.bar(['Ham', 'Spam'], class_counts, color=['blue', 'red'])
plt.xlabel('Class')
plt.ylabel('Number of Samples')
plt.title('Distribution of Spam and Ham Samples')
plt.xticks([0, 1], ['Ham', 'Spam'])
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

ham = df[df['label'] == 0]
spam = df[df['label'] == 1]

# Under-sample ham to match spam
ham_under = ham.sample(len(spam), random_state=42)
df = pd.concat([ham_under, spam]).sample(frac=1, random_state=42).reset_index(drop=True)

X = df['text']
y = df['label']

# Vectorize text data
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, shuffle=True, test_size=0.3, random_state=42)

# Train Multinomial Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)

print('Model has been trained')

# Evaluate model
y_pred = model.predict(X_test)
print('Accuracy: {:.2f}%'.format(metrics.accuracy_score(y_pred=y_pred, y_true=y_test) * 100))

confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[0, 1])
cm_display.plot()
plt.show()

# Save model and vectorizer
joblib.dump(model, r'models\sms_model.pkl')
joblib.dump(vectorizer, r'models\sms_vectorizer.pkl')


# Function to predict scam probability
def predict_scam_probability(text):
    processed_text = vectorizer.transform([text])
    probabilities = model.predict_proba(processed_text)
    scam_probability = probabilities[0][1] * 100  # Probability of 'spam' class (index 1)
    return f'Scam probability: {scam_probability:.2f}%'

# Function to extract scam keywords
def extract_scam_keywords(text, top_n=5):
    processed_text = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    coef = model.feature_log_prob_[1]  # Log-probabilities for the spam class
    word_indices = processed_text.nonzero()[1]
    word_scores = [(feature_names[i], coef[i]) for i in word_indices]
    sorted_keywords = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)
    scam_keywords = [word for word, score in sorted_keywords[:top_n]]
    return scam_keywords

# Example usage
sample_sms = "URGENT: Your account has been compromised! Please verify your identity immediately to avoid losing access. Click here: http://www.accountverify1234.com/. Failure to respond within 24 hours will result in permanent account suspension."
print(predict_scam_probability(sample_sms))
print("Detected scam keywords:", extract_scam_keywords(sample_sms))
