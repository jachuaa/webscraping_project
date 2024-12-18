import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Patterns to match in a href attributes
patterns = [
    "https://www.pursuitcollection.com",
    "https://pursuitcollection.com",
    "/Website/media/pursuit/"
]

# Load the CSV file containing the URLs
input_csv = "C:\\Users\\jachua\\OneDrive - Viad Corp\\Desktop\\webscraping\\BJC url list.csv"
output_csv = 'found_pdfs_BJC.csv'

# Read the CSV file to get the list of URLs
df = pd.read_csv(input_csv)
urls = df['url'].dropna().tolist()

# User-Agent header to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to scrape a URL and find matching PDF links
def find_matching_pdfs(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tags = soup.find_all('a')
        matching_pdfs = []

        for a in a_tags:
            href = a.get('href', '')
            if any(pattern in href for pattern in patterns) and href.lower().endswith('.pdf'):
                # Convert relative URLs to absolute URLs
                full_url = urljoin(url, href)
                matching_pdfs.append(full_url)

        return matching_pdfs

    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching {url}: {e}')
        return []

# Scrape all URLs
results = []

for url in urls:
    logging.info(f'Scraping: {url}')
    pdfs = find_matching_pdfs(url)
    for pdf_url in pdfs:
        results.append({'page_url': url, 'pdf_link': pdf_url})
    time.sleep(1)  # Delay to avoid overwhelming the server

# Save results to CSV
output_df = pd.DataFrame(results)
output_df.to_csv(output_csv, index=False)

logging.info(f'\nScraping complete! Results saved to {output_csv}')
