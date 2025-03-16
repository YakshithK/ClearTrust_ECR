import sys
import joblib
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
import numpy as np
from twilio.rest import Client

vectorizer_sms = r'.\models\sms_vectorizer.pkl'  # Change to your actual file path
model_sms = r'.\models\sms_model.pkl'  # Change to your actual file path

vectorizer_email = r'.\models\email_vectorizer.pkl'  # Change to your actual file path
model_email = r'.\models\email_model.pkl'  # Change to your actual file path

vectorizer_phone = r'.\models\phone_vectorizer.pkl'  # Change to your actual file path
model_phone = r'.\models\phone_model.pkl'  # Change to your actual file path

vectorizer = joblib.load(vectorizer_sms)
model = joblib.load(model_sms)

TWILIO_PHONE_NUMBER = "+12892778167"
FAMILY_MEMBER_PHONE = "+14374994222" 

def send_sms_alert(message):
    """Sends an SMS alert to a family member."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=FAMILY_MEMBER_PHONE
    )

def predict_sms(text, top_n=5):
    processed_text = vectorizer.transform([text])
    probabilities = model.predict_proba(processed_text)
    scam_probability = probabilities[0][1]

    feature_names = vectorizer.get_feature_names_out()
    coef = model.feature_log_prob_[1]  # Log probabilities for the spam class
    word_indices = processed_text.nonzero()[1]
    word_scores = [(feature_names[i], coef[i]) for i in word_indices]
    sorted_keywords = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)
    scam_keywords = [word for word, score in sorted_keywords[:top_n]]

    if int(scam_probability*100) > 50:
        send_sms_alert('Your family member just got a message that was most likely a scam ({0}%) : {1}. Here are the keywords: {2}.'.format(int(scam_probability*100), text, ", ".join(scam_keywords)))
        return 'This is most likely a scam ({0}%). The keywords are: {1}.'.format(int(scam_probability*100), ", ".join(scam_keywords))
    else:
        return 'This is most likely not a scam ({0}%).'.format(int(scam_probability*100))

def predict_email(text, top_n=5):
    processed_text = vectorizer.transform([text])
    probabilities = model.predict_proba(processed_text)
    scam_probability = probabilities[0][1]

    feature_names = vectorizer.get_feature_names_out()
    coef = model.feature_log_prob_[1]  # Log probabilities for the spam class
    word_indices = processed_text.nonzero()[1]
    word_scores = [(feature_names[i], coef[i]) for i in word_indices]
    sorted_keywords = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)
    scam_keywords = [word for word, score in sorted_keywords[:top_n]]

    if int(scam_probability*100) > 50:
        send_sms_alert('Your family member just got a message that was most likely a scam ({0}%) : {1}. Here are the keywords: {2}.'.format(int(scam_probability*100), text, ", ".join(scam_keywords)))
        return 'This is most likely a scam ({0}%). The keywords are: {1}.'.format(int(scam_probability*100), ", ".join(scam_keywords))
    else:
        return 'This is most likely not a scam ({0}%).'.format(int(scam_probability*100))

