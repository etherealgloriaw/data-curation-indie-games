import json
import pandas as pd
from datetime import datetime

INPUT_PATH = "igdb_pc_games.json"
OUTPUT_PATH = "igdb_clean2.csv"

def unix_to_date(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except:
        return None

def extract_genre_names(genres):
    if not isinstance(genres, list):
        return ""
    return "|".join(g.get("name","") for g in genres if g.get("name"))

# ---- Load JSON ----
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

games = data.get("games", [])
df = pd.DataFrame(games)

# ---- Transform ----
df["name"] = df["name"].fillna("").str.strip()
df["genres"] = df["genres"].apply(extract_genre_names)
df["release_date"] = df["first_release_date"].apply(unix_to_date)

# ---- Filter 2015–2025 ----
df = df.dropna(subset=["release_date"])
df["year"] = df["release_date"].str[:4].astype(int)
df = df[(df["year"] >= 2015) & (df["year"] <= 2025)]

# ---- Keep only required columns ----
df = df[["name", "genres", "release_date"]]

# ---- Export ----
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print("DONE ->", OUTPUT_PATH)