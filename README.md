# pib-articles-scraper
A simple, yet robust and efficient, Python based web scraper to compile and organize PIB Press Releases between a given period.

## Built using (dependencies):
- Python 3.x
- Libraries:
  * csv
  * beautifulsoup
  * requests
  * pandas
  * concurrent.futures

## Installation and Usage
In case any of the aforementioned required dependencies are not installed on your system, the Python script automatically installs them using pip (a package installer for Python).
Open the terminal in the installed directory and run the script by following command.

`python pib_articles_scraper.py`

The script will collect and organize the Date of Publication, Headline, Content and Link of the article released by the Press Information Bureau (PIB) in the period of January 1st, 2024 to March 31st, 2024 (can be easily modified to any other period, simply change the start and end parameters in the date_range dataframe) in a CSV file named "pib_articles.csv" in the same working directory as the python script.

## Script Overview
`articles_compiler`
This function retrieves the list of articles for a specific day from the PIB website.

Parameters:

- `day_value`: The day for which to retrieve articles.
- `month_value`: The month for which to retrieve articles.
- `year_value`: The year for which to retrieve articles.
- `session`: A requests.Session object for making HTTP requests.
Returns: A dictionary where the keys are article headlines and the values are URLs to the full articles.


`fetch_article`
This function fetches the content of an article given its URL.

Parameters:

- `link`: The URL of the article.
- `session`: A requests.Session object for making HTTP requests.
Returns: A string containing the article content.

`main`
This is the main function that orchestrates the scraping process.

- Initializes the CSV file with headers.
- Creates a requests.Session object for HTTP requests.
- Defines the date range for which to scrape articles.
- Uses a ThreadPoolExecutor to parallelize the retrieval of articles and their content.
- Writes the retrieved data to the CSV file.

## Error Handling
The script includes error handling to manage issues during the HTTP requests and parsing stages. If an error occurs while fetching articles for a specific date or content for a specific article, the error is printed to the console, and the script continues processing the next item.

## CSV Output
The output CSV file pib_articles.csv will have the following columns:

- Date of Publication: The date when the article was published.
- Headline: The headline of the article.
- Article Content: The full content of the article.
- Article Link: The URL to the article on the PIB website.

Each row in the CSV file represents a single article. The CSV file is encoded in UTF-8 with a BOM to ensure compatibility with various spreadsheet programs.
