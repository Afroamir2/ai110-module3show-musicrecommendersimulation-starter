# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeGauge 1.0** — it measures how well a song matches your vibe.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

**Goal / Task.** VibeGauge suggests songs you might like. You tell it your taste. It gives you a ranked top-5 list. Each pick comes with a short reason.

**Intended use.** This is a classroom project. It is built to learn how recommenders work. It is meant for exploring and experimenting, not for real listeners.

**Not intended for.** Do not use it in a real music app. Do not use it to make choices for real people. It runs on a tiny made-up catalog, so it cannot really know your taste.

**Assumptions.** It assumes you can name one favorite genre, one mood, an energy level, and how acoustic you like your music. It assumes those few numbers describe your taste. Real taste is much richer than that.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**Algorithm summary.** The model gives each song points. More points means a better match. It checks four things.

- Same genre as you like? Add 1 point.
- Same mood as you like? Add 1 point.
- Close to your energy level? Add up to 2 points. The closer, the more points.
- Close to how acoustic you like it? Add up to 1 point. The closer, the more points.

Then it adds up the points and sorts the songs from best to worst. It shows you the top 5.

**What I changed from the starter.** The starter gave genre 2 points and energy up to 1. I flipped that. I ran an experiment that cut genre to 1 point and raised energy to 2 points. Now energy is the most important thing. So a song with the right energy can beat a song in your favorite genre.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

**Data used.** The catalog has 18 songs. Each song has a title, artist, genre, and mood. It also has numbers for energy, tempo, valence, danceability, and acousticness. The model only uses four of these: genre, mood, energy, and acousticness.

**What genres and moods are there.** There are 15 genres, like pop, lofi, rock, jazz, and metal. Most genres have just one song. Only lofi and pop have more than one. Moods include happy, chill, intense, and sad-type moods.

**Limits of the data.** I did not add or remove any songs. The catalog is very small. The songs are also lopsided: they are either loud and electronic or quiet and acoustic, with little in between. So many real tastes, like calm electronic or energetic acoustic, are simply missing.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

**Where it works well.** It works best for clear, common tastes. A loud pop fan gets loud pop. A calm lofi fan gets calm lofi. When your taste matches songs the catalog has a lot of, the top pick is spot on.

**What it gets right.** It is good at energy. If you want high energy, you get high energy. It is also easy to trust, because every pick shows its reasons. You can see exactly why a song made the list.

**When it matched my gut.** Opposite tastes gave opposite lists. The chill fan and the rock fan shared zero songs. That felt right and showed the model was really listening to the preferences.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One clear weakness I found is that the catalog only contains two kinds of songs: loud, produced tracks and quiet, acoustic ones — there is almost nothing in between. Because of this, a listener who wants something like high-energy *acoustic* music (an energetic folk or bluegrass fan) can never get a good match, since every loud song in the dataset is also very electronic. The same problem hits people who want moderate, mid-energy music: there is a big gap in the catalog around the middle of the energy range, so those users always get pushed toward songs that are too calm or too intense for them. This bias got worse after my experiment that doubled the weight on energy, because energy became the most important factor while the catalog still couldn't serve those middle-of-the-road tastes. The unfair part is that the system never admits this — it hands these users a confident top-5 list with cheerful explanations even when nothing in the catalog actually fits what they asked for.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested three listener profiles: **High-Energy Pop** (upbeat pop, happy mood, high energy), **Chill Lofi** (mellow lofi, chill mood, low energy, warm/acoustic sound), and **Deep Intense Rock** (hard rock, intense mood, very high energy, electric sound). For each one I looked at whether the top pick actually matched the taste I described, and whether the songs lower down the list still made sense. The biggest surprise was how often the *same few high-energy songs* showed up across very different profiles — a workout song called "Gym Hero" kept appearing near the top even for the Happy Pop listener, who never asked for an "intense" workout track. The reason is that the system rewards songs for being *close in energy* to what you want, and "Gym Hero" has almost exactly the energy level all my high-energy profiles were asking for, so it sneaks onto the list even when its mood is wrong. In plain terms: the system pays a lot of attention to *how loud and fast* a song is and less to *what feeling* it carries, so energetic songs get a free pass into lots of different people's recommendations.

**High-Energy Pop vs. Chill Lofi:** These two are near-opposites, and the results reflected that cleanly — the pop listener got bright, loud, produced songs, while the lofi listener got calm, soft, acoustic ones. This pair worked exactly as intended: the two profiles want opposite energy levels and opposite sound textures, so they share basically no songs. It's the clearest sign that the system really is responding to the preferences and not just handing everyone the same list.

**High-Energy Pop vs. Deep Intense Rock:** These two look different on paper (one is happy pop, the other is intense rock) but their recommendation lists overlapped a lot, because both want very high energy. Songs like "Gym Hero" and "Pulse Republic" showed up for both, since energy is the strongest signal and both profiles sit at the loud end of the scale. This makes sense but also exposes a weakness: the system treats "happy and energetic" and "angry and energetic" as almost the same thing, because it measures energy well but understands mood only as an exact word-match.

**Chill Lofi vs. Deep Intense Rock:** This was the sharpest contrast of all — the lofi listener got the quietest, most acoustic songs in the catalog, and the rock listener got the loudest, most electric ones, with zero overlap. This is the pair I'd point to as proof the model is valid: two tastes that are opposite in both energy *and* sound texture produced two completely separate lists, which is exactly what a working recommender should do.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

**Ideas for improvement.**

1. Add more songs. Fill the gaps, like mid-energy songs and energetic acoustic songs. Right now those tastes have nothing to match.
2. Warn when the fit is weak. If the best score is low, say so. Do not hand out a confident list when nothing really fits.
3. Understand moods that are close. Right now "chill" and "relaxed" count as totally different. The model should see that some moods are cousins.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
