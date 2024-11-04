import requests
import base64
from datetime import datetime
from migration.authenticate import authenticate  # Ensure this is correct

def lipa_na_mpesa_online(phone_number, amount):
    access_token = authenticate()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = '174379'  # Replace with your Shortcode
    passkey = 'your_passkey'  # Make sure this is defined somewhere

    password = base64.b64encode(
        (business_short_code + passkey + timestamp).encode()
    ).decode('utf-8')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://your-domain.com/callback",  # Adjust this URL
        "AccountReference": "AccountTest",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    return response.json()