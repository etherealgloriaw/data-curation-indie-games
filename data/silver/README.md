Step 1 : Clean Epic Game data (epic_data_clean.py)

  - Converted raw Epic Games JSON into a CSV file
  - Mapped tag IDs to human-readable labels using the enum from the Epic API documentation
  - Filtered records to include only games with effective dates between 2015 and 2025

Step 2 : Clean Steam Game data (OpenRefine, steam_data_clean.py)

  - Removed uncessary columns in OpenRefine
  - Filtered records to include only games with effective dates between 2015 and 2025
  - Convert effective date to valid data format and filter out games not in effective range (2015-2025)
  - Convert description from json to valid string (connecting with '|' to match with epic data)
  
