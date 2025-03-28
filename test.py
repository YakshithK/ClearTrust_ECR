import joblib

# Test loading
vectorizer = joblib.load(r'.\models\sms_vectorizer.pkl')
model = joblib.load(r'.\models\sms_model.pkl')

# Test vectorizer
print("Vocabulary size:", len(vectorizer.vocabulary_))
print("IDF shape:", vectorizer.idf_.shape)

# Test with sample text
text = "This is a test message"
features = vectorizer.transform([text])
print("Features shape:", features.shape)