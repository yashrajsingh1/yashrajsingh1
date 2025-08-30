from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = "+13312677135"
your_indian_number = "+919058991119"

client = Client(account_sid, auth_token)

call = client.calls.create(
    to=your_indian_number,
    from_=twilio_number,
    url="https://2432-2401-4900-47f6-c7da-8157-7d77-4818-b84a.ngrok-free.app"
)

print(f"✅ Twilio is calling you: {call.sid}")
