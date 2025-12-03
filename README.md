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
| ipython            | 8.12.3  |
| matplotlib         | 3.10.7  |


---

## 🚀 Instructions to Reproduce the Workflow

1. Install all dependencies from the project
```bash
pip install -r requirements.txt
```
2. Click Run All for the jupyter noteboooks in the scripts folder, following the order of number in names.

   ## 1.0.5-data-collection-steam-incremental(optional).ipynb

   This one is optionally running for get the incremental refresh for steam data. Because full downloading would take a long time, we provide the option to find the difference in steam_spy_id_name by comparing the existing one to the new downloading one, and then you can jump to 1.1-data-collection-steam.ipynb and directly use the incremental list to download the newest data instead of whole data reloading from steamstore api.
   
   ## 1.1-data-collection-steam.ipynb

   This script contains 3 files output: steam_app_data.csv, steam_spy_all_data.csv and steam_spy_id_name.csv.

   The collection dependency is steam_spy_all_data.csv -> steam_spy_id_name.csv -> steam_app_data.csv.

   We use 2 APIs to finish the steam platform data collection. Thus, we first query all steam_spy api data, extracting key columns id and name, then use it as param to extract data from steam app api.

   The time needed for finishing steam_spy_all_data.csv and steam_spy_id_name.csv is around 3 minutes. However, the steam_spy_all_data.csv would take more than 10 hours with pause between each game to prevent exceeding the api limits. Therefore, we use a steam_index.txt file to record the current position and provide the functionality of downloading with several retries of notebook.

   ## 1.2-data-collection-epic.ipynb

   This script would dump all data from epic store api to a json file. The average fetching time is a couple of minutes.

   ## 1.3-data-collection-igdb.ipynb

   To run thie script, you need to get your api ID and secret from igdb api. The instruction is here: https://api-docs.igdb.com/#getting-started
   
   Then, use your own credential to fill CLIENT_ID and CLIENT_SECRET. You can also change the start and end time to set up the range of data.

   ```python
   start = int(dt.datetime(2015,1,1).timestamp())
   end   = int(dt.datetime(2025,12,31,23,59,59).timestamp())
     ```

   ## 1.4-bronze-data-EDA.ipynb

   This is the Exploratory Data Analysis for bronze layer data we just collected from steam, epic and igdb. It's optional in the whole workflow and shows the raw schema for the bronze layer.

   ## 2.1-steam_data_clean.ipynb, 2.2-epic_data_clean.ipynb, 2.3-igdb-data-clean.ipynb

   The 3 cleaning scripts flatten the nested JSON and remove the unused columns and out-of-scope time range data from bronze layer data. You can follow the script one by one or modifying the script to add any columns you want to keep.

   ## 2.4-descriptive-statistics.ipynb

   This script is running some data quality checks to compare pre-2015 and post-2025 data.

   ## 3.1-unify-gold-layer.ipynb

   This script integrates all silver layer data to one file.

   ## 3.2-indie-game-split.ipynb

   This script split the indie/non indie game from the file we deduced from 3.1.

   ## 3.3-indie-game-analysis-price.ipynb, 3.4-indie-game-analysis-platform.ipynb, 3.5-indie-game-analysis-genre.ipynb, 3.6-indie-game-analysis-publisher.ipynb, 3.7-indie-game-analysis-trend.ipynb

   The example analysis for the data we get above.
   
   Price Analysis:
   
    Compare price distributions across platforms, examine discount depth/frequency, and contrast indie vs. non-indie pricing behavior.


   Platform Analysis:
   
    Explore differences in market coverage (Steam/Epic/IGDB), exclusivity, and platform-specific characteristics such as popularity indicators, categories, and review volumes.


   Genre Analysis:
   
    Clean and standardize noisy genre labels, compute genre frequencies, and investigate which genres dominate indie vs. mainstream titles.


   Publisher Analysis:
   
    Identify top indie publishers, analyze publisher specialization, pricing strategies, and evaluate cross-platform presence.


   Trend Analysis:
   
    Use effective_date fields to study temporal patterns in releases, pricing, discounting, and shifting genre popularity over time.

---

## Dataset Metadata (JSON-LD)

```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "schemaVersion": "https://schema.org/version/15.0",
  "name": "Curated Indie Game Dataset (2015–2025)",
  "alternateName": "Indie Games Metadata: Steam, Epic Games Store, IGDB",
  "description": "Cleaned and harmonized indie game metadata aggregated from Steam, Epic Games Store, and IGDB. The dataset focuses on PC titles and includes identifiers, pricing and discount history (when available), genres, platforms, publishers/developers, release dates suitable for longitudinal analysis.",
  "url": "https://github.com/etherealgloriaw/data-curation-indie-games",
  "identifier": [
    {
      "@type": "PropertyValue",
      "propertyID": "URL",
      "value": "https://github.com/etherealgloriaw/data-curation-indie-games"
    }
  ],
  "keywords": [
    "indie games",
    "video games",
    "pricing",
    "discounts",
    "genre",
    "Steam",
    "Epic Games Store",
    "IGDB",
    "datasets",
    "data curation"
  ],
  "inLanguage": "en",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "isAccessibleForFree": true,
  "temporalCoverage": "2015-01-01/2025-12-31",
  "creator": [
    {
      "@type": "Person",
      "name": "Gloria Wang"
    },
    {
      "@type": "Person",
      "name": "Meihui Li"
    }
  ],
  "contributor": [
    {
      "@type": "Organization",
      "name": "Steam (Steam Web API & SteamSpy)"
    },
    {
      "@type": "Organization",
      "name": "Epic Games Store API"
    },
    {
      "@type": "Organization",
      "name": "IGDB"
    }
  ],
  "measurementTechnique": [
    "API-based extraction (Steam Web API, SteamSpy, Epic Games Store API, IGDB REST API)",
    "Medallion architecture (bronze/silver/gold) ETL with documented provenance",
    "Incremental refresh strategies for source updates"
  ],
   "variableMeasured": [
     {
       "@type": "PropertyValue",
       "name": "ID",
       "description": "Internal identity ID of the game (IDENTITY()).",
       "valueType": "integer"
     },
     {
       "@type": "PropertyValue",
       "name": "steam_ID",
       "description": "Identity ID of the game in Steam.",
       "valueType": "string"
     },
     {
       "@type": "PropertyValue",
       "name": "epic_ID",
       "description": "Identity ID of the game in Epic Games Store.",
       "valueType": "string"
     },
     {
       "@type": "PropertyValue",
       "name": "igdb_ID",
       "description": "Identity ID of the game in IGDB.",
       "valueType": "string"
     },
     {
       "@type": "PropertyValue",
       "name": "title",
       "description": "Title of the game.",
       "valueType": "string"
     },
     {
       "@type": "PropertyValue",
       "name": "platform",
       "description": "Platform source of the row: one or more of ['steam', 'epic', 'igdb'].",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "developers",
       "description": "Developer or developers of the game.",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "publishers_steam",
       "description": "Publisher(s) of the game on Steam.",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "publishers_epic",
       "description": "Publisher(s) of the game on Epic Games Store.",
       "valueType": "string"
     },
     {
       "@type": "PropertyValue",
       "name": "categories_steam",
       "description": "Steam categories associated with the game.",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "categories_epic",
       "description": "Epic Games Store categories associated with the game.",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "categories_igdb",
       "description": "IGDB categories associated with the game.",
       "valueType": "array[string]"
     },
     {
       "@type": "PropertyValue",
       "name": "effective_date_steam",
       "description": "Date when the record or pricing became effective on Steam.",
       "valueType": "datetime"
     },
     {
       "@type": "PropertyValue",
       "name": "effective_date_epic",
       "description": "Date when the record or pricing became effective on Epic Games Store.",
       "valueType": "datetime"
     },
     {
       "@type": "PropertyValue",
       "name": "effective_date_igdb",
       "description": "Date when the record or pricing became effective on IGDB.",
       "valueType": "datetime"
     },
     {
       "@type": "PropertyValue",
       "name": "price_steam",
       "description": "Original price before discount on Steam.",
       "valueType": "number"
     },
     {
       "@type": "PropertyValue",
       "name": "price_epic",
       "description": "Original price before discount on Epic Games Store.",
       "valueType": "number"
     },
     {
       "@type": "PropertyValue",
       "name": "discount_percent_steam",
       "description": "Discount percentage on Steam (e.g., 0.30 = 30% off).",
       "valueType": "number"
     },
     {
       "@type": "PropertyValue",
       "name": "discount_percent_epic",
       "description": "Discount percentage on Epic Games Store (e.g., 0.30 = 30% off).",
       "valueType": "number"
     }
   ],
  "distribution": [
    {
      "@type": "DataDownload",
      "name": "Repository (code, documentation, and data artifacts)",
      "contentUrl": "https://github.com/etherealgloriaw/data-curation-indie-games",
      "encodingFormat": "application/zip"
    },
    {
      "@type": "DataDownload",
      "name": "Bronze/Silver/Gold outputs (CSV/Parquet as applicable)",
      "contentUrl": "https://github.com/etherealgloriaw/data-curation-indie-games/data",
      "encodingFormat": "CSV"
    }
  ],
  "documentation": [
    "https://steamspy.com/api.php",
    "https://partner.steamgames.com/doc/webapi_overview",
    "https://epicstore-api.readthedocs.io",
    "https://api-docs.igdb.com"
  ],
  "usageInfo": "Redistribution of raw source API payloads may be restricted by respective terms of use. This repository provides curated derivatives and metadata under CC BY 4.0. Cite the project and original sources when publishing results.",
  "citation": "Wang, G., & Li, M. (2025). Curated Indie Game Dataset (2015–2025). GitHub repository: https://github.com/etherealgloriaw/data-curation-indie-games. CC BY 4.0.",
  "version": "1.0.0",
  "dateCreated": "2025-12-02",
  "provider": {
    "@type": "Organization",
    "name": "CS598 Data Curation Project",
    "url": "https://github.com/etherealgloriaw/data-curation-indie-games"
  }
}


```
