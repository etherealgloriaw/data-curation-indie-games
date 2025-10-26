#!/usr/bin/env python3
import ast
import re
import pandas as pd
from datetime import datetime
from currency_converter import CurrencyConverter

# ---------- Hard-coded paths ----------
INPUT_CSV  = "steam_raw.csv"
OUTPUT_CSV = "steam_clean5.csv"
# -------------------------------------

YEAR_MIN = 2015
YEAR_MAX = 2025
YEAR_RE  = re.compile(r"\b(\d{4})\b")

def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%d %b, %Y", "%b %d, %Y", "%d %B, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return None

def extract_date_string(cell):
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return None

    s = str(cell).strip()
    # Try dict-like
    try:
        obj = ast.literal_eval(s)
        if isinstance(obj, dict):
            if obj.get("coming_soon") is True:
                return None
            raw = (obj.get("date") or "").strip()
            date_str = parse_date(raw)
            return date_str or None
    except Exception as e:
        print(e)
        pass  # not a dict; fall through

    return s or None

def year_in_range_from_string(date_str):
    """
    Get any 4-digit year from the string and filter by YEAR_MIN..YEAR_MAX.
    If no year found, return False.
    """
    if not date_str:
        return False
    m = YEAR_RE.search(date_str)
    if not m:
        return False
    try:
        y = int(m.group(1))
        return YEAR_MIN <= y <= YEAR_MAX
    except Exception:
        return False

def dict_to_text(cell):
    """
    "[{'id': '1', 'description': 'Action'}, ...]" -> "Action|Adventure|..."
    """
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return ""
    try:
        val = ast.literal_eval(str(cell))
        if isinstance(val, list):
            parts = []
            for item in val:
                if isinstance(item, dict):
                    desc = item.get("description")
                    if desc:
                        parts.append(str(desc).strip())
            return "|".join(parts)
    except Exception:
        pass
    return ""

def coerce_int_or_empty(x):
    try:
        if x is None:
            return ""
        if isinstance(x, (int, float)) and not pd.isna(x):
            return int(x)
        xs = str(x).strip()
        return int(xs)
    except Exception:
        return ""

def parse_price_overview(cell):
    """
    "{'currency': 'USD', 'final_formatted': '$9.99', 'discount_percent': 0, ...}"
    -> (currency_code, discount_percent, final_price)
    """
    currency_code, discount_percent, final_price = "", "", ""
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return currency_code, discount_percent, final_price
    try:
        dct = ast.literal_eval(str(cell))
        if isinstance(dct, dict):
            currency_code = str(dct.get("currency", "")).strip()
            discount_percent = coerce_int_or_empty(dct.get("discount_percent"))
            raw_price = str(dct.get("final_formatted", "")).strip()
            final_price = re.sub(r"[^0-9.]", "", raw_price)

    except Exception:
        pass
    return currency_code, discount_percent, final_price

def main():
    # Read all as strings; keep blanks as ""
    currency_converter = CurrencyConverter()
    df = pd.read_csv(INPUT_CSV, dtype=str, keep_default_na=False)

    # Drop rows with blank/null-like is_free
    if "is_free" in df.columns:
        df["is_free"] = df["is_free"].astype(str)
        df = df[
            df["is_free"].str.strip().ne("") &
            df["is_free"].str.lower().ne("none") &
            df["is_free"].str.lower().ne("null")
        ].copy()

    # effective_date: extract string only (no conversion)
    df["effective_date"] = df.get("release_date", "").apply(extract_date_string)

    # Filter by year 2015..2025 based on the year number present in the string
    df = df[df["effective_date"].apply(year_in_range_from_string)].copy()
    df.drop(columns=["release_date"], inplace=True)
    df.drop(columns=["recommendations"], inplace=True)
    df.drop(columns=["platforms"], inplace=True)

    # genres -> description-only joined with "|"
    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(dict_to_text)

    if "categories" in df.columns:
        df["categories"] = df["categories"].apply(dict_to_text)

    if "platforms" in df.columns:
        df["platforms"] = df["platforms"].apply(dict_to_text)

    def safe_convert(r):
        try:
            cur = r["currency_code"]
            price = r["final_price"]
            if price is not None and cur and cur != "USD":
                res = currency_converter.convert(price, cur, "USD")
                return round(res, 2)
            return price
        except Exception as e:
            # print(e)
            return None

    # price_overview -> currency_code, discount_percent, final_price
    if "price_overview" in df.columns:
        cc, dp, fp = zip(*df["price_overview"].apply(parse_price_overview))
        df["currency_code"] = list(cc)
        df["discount_percent"] = list(dp)
        df["final_price"] = list(fp)
        df.drop(columns=["price_overview"], inplace=True)
        df["final_price_usd"] = df.apply(safe_convert, axis=1)


    # Write out
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Done. Saved {len(df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()