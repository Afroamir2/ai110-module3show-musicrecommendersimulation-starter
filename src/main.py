"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

try:
    # Works when run as a module from the repo root: `python -m src.main`
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    # Works when run directly from inside src/: `python main.py`
    from recommender import load_songs, recommend_songs

# Absolute path to data/songs.csv, resolved relative to this file so the app
# runs from any working directory (repo root or inside src/).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_CSV = os.path.join(PROJECT_ROOT, "data", "songs.csv")


# Three distinct listener taste profiles.
# Each is scored on exact-match dimensions (genre, mood) plus a numeric
# dimension scored by closeness (target_energy). See songs.csv for the values
# these profiles are tuned to match.
USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,         # upbeat, driving
        "favorite_acousticness": 0.15,  # produced, not acoustic
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,         # laid-back, low energy
        "favorite_acousticness": 0.75,  # warm, acoustic textures
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,         # heavy, high energy
        "favorite_acousticness": 0.10,  # electric, hard-hitting
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Run and print the top-5 recommendations for a single profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 48)
    print(f"  {name}")
    print(f"  Top {len(recommendations)} recommendations")
    print(f"  for a {user_prefs['favorite_genre']} / "
          f"{user_prefs['favorite_mood']} listener "
          f"(energy ~{user_prefs['target_energy']})")
    print("=" * 48)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f} / 5.00   [{song['genre']}, {song['mood']}]")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
    print()


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in USER_PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
