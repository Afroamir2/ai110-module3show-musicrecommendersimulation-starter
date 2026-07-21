# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (think Spotify or YouTube) learn what you like from huge amounts of behavior — what you play, skip, save, and replay and mix that with the qualities of the items themselves to predict what you'll enjoy next. They constantly balance relevance  against goals like freshness and variety. My version is a much smaller, transparent take on the same idea: instead of learning from behavior, it compares the measurable qualities of each song to a taste profile I describe up front, and it prioritizes matching the user's stated preferences genre, mood, and energy level over surprise or discovery. The point is not to be clever, but to make every recommendation easy to explain.

**What features each `Song` uses.** Each song carries descriptive tags and audio qualities: `genre` and `mood` (categorical), plus numeric 0–1 measures, `energy`, `valence`, `danceability`, `acousticness` and `tempo_bpm`. The scoring focuses on the most discriminative of these: `genre`, `mood`, `energy`, and `acousticness`.

**What the `UserProfile` stores.** A compact taste profile: `favorite_genre`, `favorite_mood`, a `target_energy` (the energy level the user is aiming for, not just "high" or "low"), and `likes_acoustic` (whether they lean toward acoustic sounds).

**How the `Recommender` scores each song.** It uses two rules working together:
- **Scoring rule (per song):** compares one song to the profile and returns a single number plus the reasons behind it. The point budget is:

  | Feature | Type | Rule | Points |
  |---------|------|------|--------|
  | `genre` | categorical | exact match | **+2.0** |
  | `mood` | categorical | exact match | **+1.0** |
  | `energy` | numeric | closeness to `target_energy` | **+1.0 × (1 − \|song.energy − target_energy\|)** |

  Categorical features add flat points when they match; the numeric feature rewards *closeness* to the target, so a song near the target energy scores higher than one that's simply loud or quiet. Because `energy` is already on a 0–1 scale, its contribution ranges from 0.0 to 1.0. The three parts sum to a **maximum score of 4.0**.
- **Ranking rule (across songs):** takes the whole list of scored songs, sorts by score highest-first, breaks ties, and trims to the top `k`.

**How songs get chosen.** Score every song, sort highest-first, and return the top `k` as the recommendations — each paired with a short reason built from the point awards (e.g. "matches your favorite genre (pop), matches your happy mood, and is close to your target energy").

```
songs ──[Scoring Rule]──▶ (song, score, reasons) ──[Ranking Rule]──▶ top-k recommendations
        +2 genre / +1 mood / +1 energy-closeness    sort + trim
```

**Expected biases in this design.** Because the weights are hand-chosen, they bake in predictable blind spots worth naming up front:
- **Genre over-prioritization.** Genre is worth twice as much as either other feature, so a genre match (+2.0) can never be overtaken by mood + perfect energy alone (max +2.0 combined only if both are maxed). This means the system may over-prioritize genre and overlook great songs that nail the user's mood and energy but sit in a different genre.
- **Exact-match brittleness for categories.** Genre and mood only reward *exact* string matches, so near-neighbors (`indie pop` vs `pop`, `chill` vs `relaxed`) score zero on those features even when they're a great fit — the model can't see that two labels are similar.
- **Narrow definition of taste.** Only three of the available features are scored. `valence`, `danceability`, `acousticness`, and `tempo_bpm` are ignored, so two songs that differ a lot on danceability or mood-feel can look identical to the scorer.
- **Popularity and discovery blind spot.** The system optimizes purely for similarity to the stated profile, so it never surfaces surprising or fresh picks — it will keep recommending the "safe" center of the user's taste and under-explore the catalog.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

**High-Energy Pop** — a `pop` / `happy` listener (energy ~0.9)

```
================================================
  High-Energy Pop
  Top 5 recommendations
  for a pop / happy listener (energy ~0.9)
================================================

1. Sunrise City — Neon Echo
   Score: 4.89 / 5.00   [pop, happy]
   Reasons:
     • genre match: pop (+2.0)
     • mood match: happy (+1.0)
     • energy 0.82 vs target 0.90 (+0.92)
     • acousticness 0.18 vs target 0.15 (+0.97)

2. Gym Hero — Max Pulse
   Score: 3.87 / 5.00   [pop, intense]
   Reasons:
     • genre match: pop (+2.0)
     • energy 0.93 vs target 0.90 (+0.97)
     • acousticness 0.05 vs target 0.15 (+0.90)

3. Rooftop Lights — Indigo Parade
   Score: 2.66 / 5.00   [indie pop, happy]
   Reasons:
     • mood match: happy (+1.0)
     • energy 0.76 vs target 0.90 (+0.86)
     • acousticness 0.35 vs target 0.15 (+0.80)

4. Storm Runner — Voltline
   Score: 1.94 / 5.00   [rock, intense]
   Reasons:
     • energy 0.91 vs target 0.90 (+0.99)
     • acousticness 0.10 vs target 0.15 (+0.95)

5. Pulse Republic — Kilowatt
   Score: 1.83 / 5.00   [edm, euphoric]
   Reasons:
     • energy 0.95 vs target 0.90 (+0.95)
     • acousticness 0.03 vs target 0.15 (+0.88)
```

**Chill Lofi** — a `lofi` / `chill` listener (energy ~0.4)

```
================================================
  Chill Lofi
  Top 5 recommendations
  for a lofi / chill listener (energy ~0.4)
================================================

1. Midnight Coding — LoRoom
   Score: 4.94 / 5.00   [lofi, chill]
   Reasons:
     • genre match: lofi (+2.0)
     • mood match: chill (+1.0)
     • energy 0.42 vs target 0.40 (+0.98)
     • acousticness 0.71 vs target 0.75 (+0.96)

2. Library Rain — Paper Lanterns
   Score: 4.84 / 5.00   [lofi, chill]
   Reasons:
     • genre match: lofi (+2.0)
     • mood match: chill (+1.0)
     • energy 0.35 vs target 0.40 (+0.95)
     • acousticness 0.86 vs target 0.75 (+0.89)

3. Focus Flow — LoRoom
   Score: 3.97 / 5.00   [lofi, focused]
   Reasons:
     • genre match: lofi (+2.0)
     • energy 0.40 vs target 0.40 (+1.00)
     • acousticness 0.78 vs target 0.75 (+0.97)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 2.71 / 5.00   [ambient, chill]
   Reasons:
     • mood match: chill (+1.0)
     • energy 0.28 vs target 0.40 (+0.88)
     • acousticness 0.92 vs target 0.75 (+0.83)

5. Twelve Bar Blues — Otis Grey
   Score: 1.93 / 5.00   [blues, sorrowful]
   Reasons:
     • energy 0.44 vs target 0.40 (+0.96)
     • acousticness 0.72 vs target 0.75 (+0.97)
```

**Deep Intense Rock** — a `rock` / `intense` listener (energy ~0.92)

```
================================================
  Deep Intense Rock
  Top 5 recommendations
  for a rock / intense listener (energy ~0.92)
================================================

1. Storm Runner — Voltline
   Score: 4.99 / 5.00   [rock, intense]
   Reasons:
     • genre match: rock (+2.0)
     • mood match: intense (+1.0)
     • energy 0.91 vs target 0.92 (+0.99)
     • acousticness 0.10 vs target 0.10 (+1.00)

2. Gym Hero — Max Pulse
   Score: 2.94 / 5.00   [pop, intense]
   Reasons:
     • mood match: intense (+1.0)
     • energy 0.93 vs target 0.92 (+0.99)
     • acousticness 0.05 vs target 0.10 (+0.95)

3. Pulse Republic — Kilowatt
   Score: 1.90 / 5.00   [edm, euphoric]
   Reasons:
     • energy 0.95 vs target 0.92 (+0.97)
     • acousticness 0.03 vs target 0.10 (+0.93)

4. Ironclad — Ashen Vow
   Score: 1.89 / 5.00   [metal, aggressive]
   Reasons:
     • energy 0.97 vs target 0.92 (+0.95)
     • acousticness 0.04 vs target 0.10 (+0.94)

5. Sunrise City — Neon Echo
   Score: 1.82 / 5.00   [pop, happy]
   Reasons:
     • energy 0.82 vs target 0.92 (+0.90)
     • acousticness 0.18 vs target 0.10 (+0.92)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



