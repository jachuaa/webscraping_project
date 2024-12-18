import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

# Patterns to match in attributes
patterns = [
    "https://www.pursuitcollection.com",
    "https://pursuitcollection.com",
    "/Website/media/pursuit/",
    "/styles/themes/"
]

# File extensions to look for
file_extensions = ('.svg', '.jpeg', '.jpg', '.png', '.gif', '.css')

# Load the CSV file containing the URLs
input_csv = "C:\\Users\\jachua\\OneDrive - Viad Corp\\Desktop\\webscraping\\BJC url list.csv"
output_csv = 'found_files_BJC.csv'

# Read the CSV file to get the list of URLs
df = pd.read_csv(input_csv)
urls = df['url'].dropna().tolist()

# Function to scrape a URL and find matching files in any attribute
def find_matching_files(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        matching_files = []

        # Iterate through all elements and all attributes
        for element in soup.find_all(True):  # True finds all tags
            for attr, attr_value in element.attrs.items():
                # Check if the attribute value is a string or list (some attributes can be lists)
                if isinstance(attr_value, str):
                    values = [attr_value]
                elif isinstance(attr_value, list):
                    values = attr_value
                else:
                    continue

                # Check each value for patterns and file extensions
                for value in values:
                    if any(pattern in value for pattern in patterns) and value.endswith(file_extensions):
                        full_url = urljoin(url, value)
                        matching_files.append({'tag': element.name, 'attribute': attr, 'file_url': full_url})

        return matching_files

    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return []

# Scrape all URLs
results = []

for url in urls:
    print(f'Scraping: {url}')
    files = find_matching_files(url)
    for file_info in files:
        results.append({'page_url': url, 'tag': file_info['tag'], 'attribute': file_info['attribute'], 'file_src': file_info['file_url']})
    time.sleep(1)  # Delay to avoid overwhelming the server

# Save results to CSV
output_df = pd.DataFrame(results)
output_df.to_csv(output_csv, index=False)

print('\nScraping complete! Results saved to found_files_BJC.csv')
