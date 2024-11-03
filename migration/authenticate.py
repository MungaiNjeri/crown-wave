import requests
from flask import Flask, jsonify
from config import app

# Mpesa API credentials
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'

def authenticate():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response['access_token']
        return access_token
    else:
        raise Exception("Failed to authenticate with Mpesa API")

@app.route('/authenticate', methods=['GET'])
def get_token():
    try:
        access_token = authenticate()
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)