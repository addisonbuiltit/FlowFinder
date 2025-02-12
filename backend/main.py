from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Sample data (temporary)
songs_db = [
    {"title": "Song A", "artist": "Artist 1", "key": "C", "bpm": 120},
    {"title": "Song B", "artist": "Artist 2", "key": "G", "bpm": 128},
    {"title": "Song C", "artist": "Artist 3", "key": "C", "bpm": 120},
]

# Input model
class SongRequest(BaseModel):
    key: str
    bpm: int

@app.post("/match", response_model=List[dict])
def match_songs(song: SongRequest):
    matched_songs = [s for s in songs_db if s["key"] == song.key and s["bpm"] == song.bpm]
    return matched_songs
