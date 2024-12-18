import os
import requests
import webbrowser
from dotenv import load_dotenv

class StravaAuthenticator:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.client_id = os.getenv('STRAVA_CLIENT_ID')
        self.client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        self.redirect_uri = os.getenv('STRAVA_REDIRECT_URI')
        
        # Ensure credentials are set
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Please set STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, and STRAVA_REDIRECT_URI in .env file")

    def get_authorization_url(self):
        """Generate Strava OAuth authorization URL"""
        return (
            f"https://www.strava.com/oauth/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&scope=activity:read_all"
        )

    def exchange_token(self, code):
        """Exchange authorization code for access token"""
        token_url = "https://www.strava.com/oauth/token"
        response = requests.post(token_url, data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code"
        })
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    def authenticate(self):
        """Full authentication flow"""
        # Open authorization URL
        auth_url = self.get_authorization_url()
        webbrowser.open(auth_url)
        
        # Prompt for authorization code
        print("\n🚀 Strava Authorization\n")
        print("1. A browser window has opened for Strava authorization.")
        print("2. After authorizing, you'll be redirected to a URL.")
        print("3. Copy the ENTIRE URL from your browser.")
        auth_code = input("\nEnter the FULL redirect URL: ").split("code=")[1].split("&")[0]
        
        # Exchange code for tokens
        tokens = self.exchange_token(auth_code)
        
        return {
            "access_token": tokens['access_token'],
            "refresh_token": tokens['refresh_token'],
            "expires_at": tokens['expires_at']
        }

def save_tokens(tokens):
    """Save tokens securely"""
    with open("strava_tokens.json", "w") as f:
        json.dump(tokens, f)

if __name__ == "__main__":
    import json
    authenticator = StravaAuthenticator()
    tokens = authenticator.authenticate()
    save_tokens(tokens)
    print("\n✅ Authentication Successfull!")