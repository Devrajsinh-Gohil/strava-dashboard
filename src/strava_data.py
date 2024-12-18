import os
import json
import requests
import pandas as pd
from datetime import datetime

class StravaDataFetcher:
    def __init__(self, tokens_file="strava_tokens.json"):
        # Load tokens
        with open(tokens_file, 'r') as f:
            self.tokens = json.load(f)
        
        # Check token expiration
        if datetime.now().timestamp() >= self.tokens['expires_at']:
            self._refresh_token()

    def _refresh_token(self):
        """Refresh access token if expired"""
        from .auth_script import StravaAuthenticator
        authenticator = StravaAuthenticator()
        new_tokens = authenticator.exchange_token(self.tokens['refresh_token'])
        
        # Update tokens
        self.tokens = {
            "access_token": new_tokens['access_token'],
            "refresh_token": new_tokens['refresh_token'],
            "expires_at": new_tokens['expires_at']
        }
        
        # Save updated tokens
        with open("strava_tokens.json", "w") as f:
            json.dump(self.tokens, f)

    def get_activities(self, limit=30):
        """Fetch Strava activities"""
        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {self.tokens['access_token']}"}
        params = {"per_page": limit}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
            
            activities = response.json()
            
            # Check if activities list is empty
            if not activities:
                
                print("Warning: No activities returned from Strava API")
            
            return activities
        
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error fetching activities: {e}")
            raise

    def process_activities(self, activities):
        """Process raw Strava activities into a DataFrame"""
        processed_data = []
        for activity in activities:
            processed_data.append({
                "name": activity.get("name", "Unnamed Activity"),
                "type": activity.get("type", "Unknown"),
                "start_date": datetime.fromisoformat(activity.get("start_date", "").replace('Z', '+00:00')),
                "distance_km": round(activity.get("distance", 0) / 1000, 2),
                "moving_time_min": round(activity.get("moving_time", 0) / 60, 2),
                "total_elevation_gain": round(activity.get("total_elevation_gain", 0), 2),
                "average_speed_kmh": round(activity.get("average_speed", 0) * 3.6, 2),
                "average_heartrate": activity.get("average_heartrate", None),
                "max_heartrate": activity.get("max_heartrate", None)
            })
        return pd.DataFrame(processed_data)
    
    def get_athlete_profile(self):
        """Fetch athlete profile information"""
        url = "https://www.strava.com/api/v3/athlete"
        headers = {"Authorization": f"Bearer {self.tokens['access_token']}"}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
            
            athlete_profile = response.json()
            return {
                "name": f"{athlete_profile.get('firstname', '')} {athlete_profile.get('lastname', '')}".strip(),
                "username": athlete_profile.get('username'),
                "profile_image": athlete_profile.get('profile'),
                "total_followers": athlete_profile.get('follower_count'),
                "total_friends": athlete_profile.get('friend_count')
            }
        
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error fetching athlete profile: {e}")
            raise