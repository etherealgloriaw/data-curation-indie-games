1. Clean Epic Games data (epic_data_clean.py)
- Mapped tag IDs to human-readable labels using the enum from the Epic API documentation
- Filtered records to include only games with effective dates between 2015 and 2025
- Price values were cleaned by removing currency symbols such as “$”. Price values were cleaned by removing currency symbols such as “$”.

2. Clean Steam Games data (OpenRefine, steam_data_clean.py)
Step 1. In OpenRefine, removed unnecessary columns and renamed the remaining ones. Exported the file as csv.
Step 2. Use python script to clean the data
  - Dropped rows with a null is_free value, as those records consistently lacked valid information. 
  - Extracted currency code, discount percent and final price into separate columns
  - Converted each final price to USD using a currency converter and put the converted price value in final_price_usd column
  - Normalized the effectiveDate column to a valid date format, filters rows by year range 2015–2025 using a year extracted from a date field

3. Clean IGDB data (igdb_clean.py)
- Converted Unix timestamps to readable dates in YYYY-MM-DD format
- Extracted genre names from genre IDs and joins them into a single string
- Standardized the game name column (fill blanks, trim spaces)
- Created a release year column and filters games to only those released between 2015 and 2025
- Kept only three columns: name, genres, and release_date
