# data-curation-indie-games

### CS598 — Data Curation Course Project  
**Authors:** Gloria Wang, Meihui Li

---

## 🖥️ Computational Environment

### Base Image
python:3.12.1

shell
Copy code

### Server
Docker Desktop 4.52.0 (210994)

Engine:
Version: 29.0.1
API version: 1.52 (minimum 1.44)
Go version: go1.25.4
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

```bash
docker build -t myproject .
docker run -p 8000:8000 --env-file .env myproject
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
