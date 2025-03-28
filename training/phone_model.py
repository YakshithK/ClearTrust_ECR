import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  # Importing Multinomial Naive Bayes
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r'data\phone.csv')

X = df['text']
y = df['label']

# Vectorize text data
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, shuffle=True, test_size=0.3, random_state=42)

# Use Multinomial Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)

print('Model has been trained')

# Evaluate the model
y_pred = model.predict(X_test)

print('Accuracy: {:.2f}%'.format(metrics.accuracy_score(y_pred=y_pred, y_true=y_test) * 100))

# Confusion Matrix
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[0, 1])
cm_display.plot()
plt.show()

# Save the trained model and vectorizer
joblib.dump(model, r'models\phone_model.pkl')
joblib.dump(vectorizer, r'models\phone_vectorizer.pkl')
