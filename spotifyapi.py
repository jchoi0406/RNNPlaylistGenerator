import requests
import os
import pandas as pd
import base64
from dotenv import main
main.load_dotenv()

api_key = os.getenv("SPOTIFY_KEY")
api_secret = os.getenv("SPOTIFY_SECRET")
df = pd.read_csv("alltracks.csv")

def authenticate(api_key, api_secret):
    auth_string = f"{api_key}:{api_secret}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.json().get("access_token")

import requests

def get_spotify_tracks(df, token):
    song_ids = []  # Initialize an empty list to store track IDs

    for index, row in df.iterrows():
        query = f"{row['track_name']} {row['artist']}"
        print(query)
        url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            tracks = response.json().get('tracks', {}).get('items', [])
            if tracks:
                track_id = tracks[0].get('id')
                song_ids.append(track_id)
            else:
                song_ids.append(None) 

        except requests.exceptions.RequestException as e:
            print(f"Error fetching track ID for {query}: {e}")
            song_ids.append(None)  
    df['track_ids'] = song_ids

    return df

    

token = authenticate(api_key, api_secret)
new_df = get_spotify_tracks(df, token)
print(new_df)