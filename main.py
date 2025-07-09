import os
import requests
from moviepy.editor import *
from elevenlabs import generate, save, set_api_key

# Setup
set_api_key(os.environ['ELEVENLABS_API_KEY'])

# Get Reddit post
def get_reddit_post():
    headers = {"User-Agent": os.environ['REDDIT_USER_AGENT']}
    auth = requests.auth.HTTPBasicAuth(os.environ['REDDIT_CLIENT_ID'], os.environ['REDDIT_CLIENT_SECRET'])

    data = {
        'grant_type': 'password',
        'username': os.environ.get("REDDIT_USERNAME"),
        'password': os.environ.get("REDDIT_PASSWORD")
    }

    token = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers).json()['access_token']
    headers['Authorization'] = f'bearer {token}'

    res = requests.get("https://oauth.reddit.com/r/AskReddit/top?limit=1&t=day", headers=headers)
    post = res.json()['data']['children'][0]['data']
    return post['title'], post['selftext']

# Generate Voice
def generate_voice(text):
    audio = generate(text=text, voice="Bella", model="eleven_monolingual_v1")
    save(audio, "output.mp3")

# Create Video
def create_video(text):
    txt_clip = TextClip(text, fontsize=50, color='white', size=(720, 1280), method='caption')
    txt_clip = txt_clip.set_duration(10)
    audio = AudioFileClip("output.mp3")
    video = txt_clip.set_audio(audio)
    video.write_videofile("output.mp4", fps=24)

if __name__ == "__main__":
    title, body = get_reddit_post()
    full_text = title + "\n" + body
    generate_voice(full_text)
    create_video(full_text)
