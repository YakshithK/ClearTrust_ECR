import os
from dotenv import load_dotenv

load_dotenv()

openapi_key = os.getenv('OPENAPI_KEY')
project_id = os.getenv('PROJECT_ID')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')