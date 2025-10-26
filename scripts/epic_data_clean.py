import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------- HARD-CODED PATHS ----------
INPUT_PATH  = Path(r"epic_games_all.json")   # change if needed
OUTPUT_PATH = Path(r"epic_games_clean7.csv")    # change if needed
# --------------------------------------

# Tag ID -> human-readable label
TAG_ID_TO_LABEL = {
    "1216": "Action games",
    "1117": "Adventure games",
    "9559": "Editors for games",
    "1203": "Multiplayer games",
    "9548": "Games for OSX (Mac OS)",
    "1298": "Puzzle games",
    "1212": "Racing games",
    "1367": "RPG games",
    "1210": "Shooter games",
    "1370": "Single-player games",
    "1115": "Strategy games",
    "1080": "Survival games",
    "9547": "Games for Windows",
}

def valid_year(iso_str):
    try:
        y = datetime.fromisoformat(iso_str.replace("Z","")).year
        return 2015 <= y <= 2025
    except:
        return False

def extract_row(item: dict) -> dict:
    # Map tags to readable labels; ignore unknown IDs
    labels = []
    for t in item.get("tags") or []:
        if isinstance(t, dict) and "id" in t:
            lbl = TAG_ID_TO_LABEL.get(str(t["id"]))
            if lbl:
                labels.append(lbl)
    tags_joined = "|".join(labels)

    # customAttributes: keep keys where value is true/"true"
    true_keys = []
    for c in item.get("customAttributes") or []:
        if not isinstance(c, dict):
            continue
        val = c.get("value")
        if (isinstance(val, str) and val.lower() == "true") or (val is True):
            if c.get("key"):
                true_keys.append(str(c["key"]))
    custom_true_joined = "|".join(true_keys)

    # price fields (no flatten): numeric original/discount + fmt intermediate + currency code
    tp = (item.get("price") or {}).get("totalPrice") or {}
    fmt = tp.get("fmtPrice") or {}

    return {
        "title": item.get("title"),
        "effective_date": item.get("effectiveDate"),
        "seller_name": (item.get("seller") or {}).get("name"),
        "tags_joined": tags_joined,
        "original_price": fmt.get("originalPrice"),
        "discount_price": fmt.get("discountPrice"),
        "intermediate_price": fmt.get("intermediatePrice"),
        "currency_code": tp.get("currencyCode"),
    }

# ---------- load JSON (object or list) ----------
text = INPUT_PATH.read_text(encoding="utf-8").strip()
data = json.loads(text)
if isinstance(data, dict):
    data = [data]

rows = [extract_row(obj) for obj in data]
df = pd.DataFrame(rows)
df = df[df["effective_date"].apply(valid_year)]

# convert date format
df["effective_date"] = pd.to_datetime(df["effective_date"], utc=True).dt.strftime("%Y-%m-%d")

# make price column display numeric value
df["original_price"] = df["original_price"].str.replace("$", "", regex=False)
df["discount_price"] = df["discount_price"].str.replace("$", "", regex=False)
df["intermediate_price"] = df["intermediate_price"].str.replace("$", "", regex=False)

df = df[[
    "title",
    "effective_date",
    "seller_name",
    "tags_joined",
    "original_price",
    "discount_price",
    "intermediate_price",
    "currency_code"
]]

df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print(f"CSV saved to: {OUTPUT_PATH}")