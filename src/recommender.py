import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    favorite_acousticness: float  # 0.0 (produced) - 1.0 (acoustic)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Songs for this user, best-scoring first."""
        prefs = _profile_to_prefs(user)
        scored = [
            (song, score_song(prefs, _song_to_dict(song))[0])
            for song in self.songs
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain, in one line, why this song fits (or doesn't fit) the user."""
        prefs = _profile_to_prefs(user)
        score, reasons = score_song(prefs, _song_to_dict(song))
        detail = "; ".join(reasons) if reasons else "no strong matches"
        return f"{song.title} scored {score:.2f} — {detail}"


# --- Helpers bridging the dataclass API to the dict-based scoring ----------

def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass into the dict shape score_song() expects."""
    return {
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "acousticness": song.acousticness,
    }


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dict score_song() expects."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "favorite_acousticness": user.favorite_acousticness,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file into a list of dicts, converting numeric fields to floats.
    """
    # Columns that must become floats for the scoring math.
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song["id"] = int(song["id"])
            for field in float_fields:
                song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences, returning (score, reasons)."""
    # Algorithm Recipe (see README "How The System Works"):
    #   +1.0  genre match                                  (halved: was +2.0)
    #   +1.0  mood match
    #   +2.0 * (1 - |song.energy - target_energy|)         for energy closeness (doubled: was +1.0)
    #   +1.0 * (1 - |song.acousticness - favorite_acousticness|)  for acoustic fit
    # Max score = 5.0. Returns (score, reasons); each reason names its points
    # so the user understands why a song was recommended.
    score = 0.0
    reasons: List[str] = []

    # Genre: exact match, +1.0 (halved for the energy-forward experiment).
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append(f"genre match: {song['genre']} (+1.0)")

    # Mood: exact match, +1.0.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Energy: reward closeness to the target (energy is on a 0-1 scale),
    # weighted x2.0 so energy fit is now the dominant signal.
    energy_points = 2.0 * (1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target "
        f"{user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
    )

    # Acousticness: reward closeness to the preferred acoustic level (0-1 scale).
    acoustic_points = 1.0 - abs(song["acousticness"] - user_prefs["favorite_acousticness"])
    score += acoustic_points
    reasons.append(
        f"acousticness {song['acousticness']:.2f} vs target "
        f"{user_prefs['favorite_acousticness']:.2f} (+{acoustic_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), best first."""
    # 1. Judge every song in the catalog with score_song().
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # 2. Rank highest-first and keep the top k in one expression.
    #    sorted() returns a new list (so it can be sliced directly), unlike
    #    list.sort() which sorts in place and returns None.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
