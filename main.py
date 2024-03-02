from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv()

CLIENT_ID = "983ce0171e47440a85a509b203a311a7"
CLIENT_SECRET = "97c2192c7bba43f2bd81cfb1b93dbaf7"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
limit = 1

# creating access to the authorization token 
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token  = json_result["access_token"]
    return token

# constructs the header needed 
def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

# search for desired artist -
def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # query = f"q={artist_name}&type=artist&limit=1"
    # query_url = url + query
    params = {"q": artist_name, "type": "artist", "limit": limit}
    result = get(url, headers = headers, params=params)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print("no artist with this name exist...oopsie")
        return None
    return json_result[0]
    # print(json_result)
    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)["tracks"]
        return json_result
    else:
        print(f"Error: {result.status_code}")
        return None

token = get_token()
result = search_artist(token, "BTS")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

#parsing artist info to get top 10 songs 
for i, song in enumerate(songs):
    print(f"{i+1}. {song['name']}")

    
    

