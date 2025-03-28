import sys
import joblib
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
import numpy as np
from twilio.rest import Client
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# File paths
MODEL_DIR = './models'
SMS_FILES = {
    'vectorizer': os.path.join(MODEL_DIR, 'sms_vectorizer.pkl'),
    'model': os.path.join(MODEL_DIR, 'sms_model.pkl')
}
EMAIL_FILES = {
    'vectorizer': os.path.join(MODEL_DIR, 'email_vectorizer.pkl'),
    'model': os.path.join(MODEL_DIR, 'email_model.pkl')
}

# Simple fallback vectorizer in case loaded models fail
fallback_vectorizer = TfidfVectorizer()
fallback_vectorizer.fit(['this is a dummy text to initialize the vectorizer'])

TWILIO_PHONE_NUMBER = "+12892778167"
FAMILY_MEMBER_PHONE = "+14374994222" 

def send_sms_alert(message):
    """Sends an SMS alert to a family member."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=FAMILY_MEMBER_PHONE
        )
    except Exception as e:
        print(f"Failed to send SMS alert: {e}")

def get_scam_keywords(vectorizer, model, processed_text, top_n=5):
    """Extract keywords that indicate scam potential."""
    try:
        feature_names = vectorizer.get_feature_names_out()
        coef = model.feature_log_prob_[1]
        word_indices = processed_text.nonzero()[1]
        word_scores = [(feature_names[i], coef[i]) for i in word_indices]
        sorted_keywords = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)
        return [word for word, score in sorted_keywords[:top_n]]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def predict_scam(text, vectorizer, model, scam_type="message", top_n=5):
    """Generic prediction function for both SMS and email."""
    try:
        if not text.strip():
            return f"Cannot analyze empty {scam_type}"

        # Debug prints
        print(f"Vectorizer type: {type(vectorizer)}")
        print(f"Model type: {type(model)}")
        
        # Check if vectorizer is fitted
        try:
            processed_text = vectorizer.transform([text])
        except Exception as ve:
            print(f"Vectorizer error: {ve}")
            print("Using fallback vectorizer...")
            processed_text = fallback_vectorizer.transform([text])

        # Simple probability calculation
        try:
            probabilities = model.predict_proba(processed_text)
            scam_probability = probabilities[0][1]
        except Exception as me:
            print(f"Model prediction error: {me}")
            return "Unable to make prediction at this time."

        probability_percentage = int(scam_probability * 100)

        scam_keywords = get_scam_keywords(vectorizer, model, processed_text, top_n)

        if probability_percentage > 50:
            alert_message = (
                f'Your family member just got a {scam_type} that was most likely '
                f'a scam ({probability_percentage}%): {text}. '
                f'Keywords: {", ".join(scam_keywords)}.'
            )
            send_sms_alert(alert_message)
            return f'This is most likely a scam ({probability_percentage}%). Keywords: {", ".join(scam_keywords)}.'
        else:
            return f'This is most likely not a scam ({probability_percentage}%).'

    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Sorry, there was an error analyzing this message."

# Load models with error handling
try:
    print("Loading SMS models...")
    vectorizer_sms = joblib.load(SMS_FILES['vectorizer'])
    model_sms = joblib.load(SMS_FILES['model'])
    print("SMS models loaded successfully")
    
    print("Loading email models...")
    vectorizer_email = joblib.load(EMAIL_FILES['vectorizer'])
    model_email = joblib.load(EMAIL_FILES['model'])
    print("Email models loaded successfully")
    
except FileNotFoundError as e:
    print(f"Error loading model files: {e}")
    # Initialize with fallback
    vectorizer_sms = vectorizer_email = fallback_vectorizer
    model_sms = model_email = None
except Exception as e:
    print(f"Unexpected error loading models: {e}")
    vectorizer_sms = vectorizer_email = fallback_vectorizer
    model_sms = model_email = None

def predict_sms(text, top_n=5):
    """Predict if an SMS is a scam."""
    if model_sms is None:
        return "SMS scam detection model is not available."
    return predict_scam(text, vectorizer_sms, model_sms, "SMS", top_n)

def predict_email(body, top_n=5):
    """Predict if an email is a scam."""
    if model_email is None:
        return "Email scam detection model is not available."
    return predict_scam(body, vectorizer_email, model_email, "email", top_n)

