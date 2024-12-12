import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

# Patterns to match in img src attributes
patterns = [
    "https://www.pursuitcollection.com",
    "https://pursuitcollection.com",
    "/Website/media/pursuit/"
]

# Load the CSV file containing the URLs
input_csv = "C:\\Users\\jachua\\OneDrive - Viad Corp\\Desktop\\webscraping\\FOLV url new list.csv" # Ensure this file is in the same folder
output_csv = 'found_images_FOLV_new.csv'

# Read the CSV file to get the list of URLs
df = pd.read_csv(input_csv)
urls = df['url'].dropna().tolist()

# Function to scrape a URL and find matching images
def find_matching_images(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img')
        matching_images = []

        for img in img_tags:
            src = img.get('src', '')
            if any(pattern in src for pattern in patterns):
                # Convert relative URLs to absolute URLs
                full_url = urljoin(url, src)
                matching_images.append(full_url)

        return matching_images

    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return []

# Scrape all URLs
results = []

for url in urls:
    print(f'Scraping: {url}')
    images = find_matching_images(url)
    for img_url in images:
        results.append({'page_url': url, 'image_src': img_url})
    time.sleep(1)  # Delay to avoid overwhelming the server

# Save results to CSV
output_df = pd.DataFrame(results)
output_df.to_csv(output_csv, index=False)

print('\nScraping complete! Results saved to found_images_FOLV_new.csv')
