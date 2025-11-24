# data-curation-indie-games

### CS598 — Data Curation Course Project  
**Authors:** Gloria Wang, Meihui Li

---

## 🖥️ Computational Environment

### Base Image
python:3.12.1
OS/Arch: linux/amd64

### Internal Dependencies (from `requirements.txt`)
| Package            | Version |
|--------------------|---------|
| pandas             | 2.3.3   |
| numpy              | 2.3.5   |
| epicstore_api      | 0.2     |
| requests           | 2.32.5  |
| currencyconverter  | 0.8.12  |

---

## 🚀 Instructions to Reproduce the Workflow

1. Install all dependencies from the project
```bash
pip install -r requirements.txt
```
2. Click Run All for the jupyter noteboooks in the scripts folder, following the order of number in names.
   
   1.1-data-collection-steam.ipynb

   This script contains 3 files output: steam_app_data.csv, steam_spy_all_data.csv and steam_spy_id_name.csv.

   The collection dependency is steam_spy_all_data.csv -> steam_spy_id_name.csv -> steam_app_data.csv.

   We use 2 APIs to finish the steam platform data collection. Thus, we first query all steam_spy api data, extracting key columns id and name, then use it as param to extract data from steam app api.

   The time needed for finishing steam_spy_all_data.csv and steam_spy_id_name.csv is around 3 minutes. However, the steam_spy_all_data.csv would take more than 10 hours with pause between each game to prevent exceeding the api limits. Therefore, we use a steam_index.txt file to record the current position and provide the functionality of downloading with several retries of notebook.

   1.2-data-collection-epic.ipynb

   This script would dump all data from epic store api to a json file. The average fetching time is 3 minutes.

   1.3-data-collection-igdb.ipynb

   To run thie script, you need to get your api ID and secret from igdb api. The instruction is here: https://api-docs.igdb.com/#getting-started
   
   Then, use your own credential to fill CLIENT_ID and CLIENT_SECRET. You can also change the start and end time to set up the range of data.

   ```python
start = int(dt.datetime(2015,1,1).timestamp())
end   = int(dt.datetime(2025,12,31,23,59,59).timestamp())
  ```

---

## Dataset Metadata (JSON-LD)

```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "name": "Curated Indie Game Dataset (2015-2025)",
  "description": "A cleaned and harmonized dataset of indie game metadata from Steam, Epic Games Store, and IGDB.",
  "creator": [
    {"@type": "Person", "name": "Gloria Wang"},
    {"@type": "Person", "name": "Meihui Li"}
  ],
  "temporalCoverage": "2015-01-01/2025-12-31",
  "license": "CC BY 4.0",
  "keywords": ["indie games", "pricing", "genre", "popularity"],
  "distribution": {
    "@type": "DataDownload",
    "contentUrl": "https://github.com/etherealgloriaw/data-curation-indie-games",
    "encodingFormat": "CSV"
  },
  "variableMeasured": []
}
```
