from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

songs_db = [
    {"title": "Song A", "artist": "Artist 1", "key": "C", "bpm": 120, "genre": "House", "energy": 8},
    {"title": "Song B", "artist": "Artist 2", "key": "G", "bpm": 128, "genre": "Techno", "energy": 9},
    {"title": "Song C", "artist": "Artist 3", "key": "C", "bpm": 120, "genre": "House", "energy": 6},
    {"title": "Song D", "artist": "Artist 4", "key": "C", "bpm": 120, "genre": "House", "energy": 7}
]


class SongRequest(BaseModel):
    key: str
    bpm: int
    genre: Optional[str] = None
    energy: Optional[int] = None  # 1 (low) to 10 (high)
    energy_sensitivity: Optional[int] = 0  # 0 = exact match, higher = allows close matches

@app.post("/match", response_model=List[dict])
def match_songs(song: SongRequest):
    matched_songs = [
        s for s in songs_db
        if s["key"] == song.key and s["bpm"] == song.bpm
    ]
    
    # Apply genre filter if provided
    if song.genre:
        matched_songs = [s for s in matched_songs if s.get("genre") == song.genre]
    
    # Apply energy filter with sensitivity if provided
    if song.energy is not None:
        matched_songs = [
            s for s in matched_songs
            if abs(s.get("energy", 0) - song.energy) <= song.energy_sensitivity
        ]

    return matched_songs

