"""
Google Drive to YouTube Uploader
Run this script in Google Colab for maximum speed.
"""

# ==========================================
# PART 1: Install Required Libraries
# (Run this first in Colab)
# ==========================================
# !pip install google-api-python-client google-auth-oauthlib google-auth-httplib2


# ==========================================
# PART 2: Single Video Upload (Standard)
# ==========================================
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow

def upload_single_video():
    video_path = "/content/drive/MyDrive/video.mp4" 
    video_title = "Your Video Title"
    video_description = "Uploaded via Colab"

    flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['https://www.googleapis.com/auth/youtube.upload'], redirect_uri='https://google.com')
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("1. Verify here:", auth_url)
    code = input("\n2. Paste code: ")
    flow.fetch_token(code=code)
    
    youtube = build('youtube', 'v3', credentials=flow.credentials)
    print("Uploading...")
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": video_title, "description": video_description, "categoryId": "22"}, "status": {"privacyStatus": "private"}},
        media_body=MediaFileUpload(video_path)
    )
    request.execute()
    print("✅ Upload completed!")


# ==========================================
# PART 3: Large Video Upload (Chunked)
# ==========================================
def upload_large_video_in_chunks():
    video_path = "/content/drive/MyDrive/large_video.mp4" 
    chunk_size_mb = 256 # Best for Colab speed

    flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['https://www.googleapis.com/auth/youtube.upload'], redirect_uri='https://google.com')
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("1. Verify here:", auth_url)
    code = input("\n2. Paste code: ")
    flow.fetch_token(code=code)
    
    youtube = build('youtube', 'v3', credentials=flow.credentials)
    media = MediaFileUpload(video_path, chunksize=chunk_size_mb * 1024 * 1024, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": "Large Video", "categoryId": "22"}, "status": {"privacyStatus": "private"}},
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")
    print("✅ Large upload completed!")


# ==========================================
# PART 4: Batch/Folder Upload (Multiple Videos)
# ==========================================
def upload_folder_batch():
    folder_path = "/content/drive/MyDrive/VideoFolder" 

    flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['https://www.googleapis.com/auth/youtube.upload'], redirect_uri='https://google.com')
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("1. Verify here:", auth_url)
    code = input("\n2. Paste code: ")
    flow.fetch_token(code=code)
    youtube = build('youtube', 'v3', credentials=flow.credentials)
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp4"):
            full_path = os.path.join(folder_path, file_name)
            video_title = file_name.replace(".mp4", "")
            print(f"Uploading: {file_name} ...")
            
            request = youtube.videos().insert(
                part="snippet,status",
                body={"snippet": {"title": video_title, "categoryId": "22"}, "status": {"privacyStatus": "private"}},
                media_body=MediaFileUpload(full_path)
            )
            request.execute()
            print(f"✅ Success: {file_name}")
    print("✅ All videos uploaded successfully!")
