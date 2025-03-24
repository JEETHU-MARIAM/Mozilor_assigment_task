import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from urllib.parse import urlparse

def extract_website_data(url):
    """
    Extracts text content from a website, cleans it, and returns it along with the URL.

    Args:
        url (str): The URL of the website.

    Returns:
        tuple: A tuple containing the URL and the cleaned text content, or (None, None) if an error occurs.
    """
    try:
        response = requests.get(url, timeout=10)  # Added a timeout
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)  # Extract text with spaces and strip whitespace

        # Clean the text (remove unwanted characters, etc.)
        text = re.sub(r'\[.*?\]', '', text)  # Remove text within square brackets
        text = re.sub(r'[^\w\s]', ' ', text)  # Replace punctuation with spaces
        text = re.sub(r'\w*\d\w*', '', text)  # Remove words containing numbers
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces

        return url, text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None, None

def save_data_to_csv(data, filename="website_data.csv"):
    """
    Saves website data (URL and text) to a CSV file.

    Args:
        data (list): A list of tuples, where each tuple contains (URL, text).
        filename (str): The name of the CSV file to save to.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["URL", "Text", "email"])  # Write header row
            writer.writerows(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def is_valid_url(url):
    """
    Checks if a URL is valid using basic parsing.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Must have scheme and netloc
    except:
        return False

if __name__ == "__main__":
     # Replace with your list of URLs
    website_urls = [
        {"url": "https://www.digitalsilk.com/", "recipient_email": "mariambiju22@gmail.com"},
        {"url": "https://www.baunfire.com/", "recipient_email": "jeethumariam02@gmail.com"},
        {"url":"https://fourbynorth.com/","recipient_email":"mariambiju22@gmail.com"},
        {"url":"https://www.geeksforgeeks.org/","recipient_email":"jeethumariam02@gmail.com"},
    ]
    extracted_data = []
    for agencies in website_urls:
        url = agencies["url"]
        recipient_email = agencies["recipient_email"]
        if is_valid_url(url):  # Check if the URL is valid before processing
            print(f"Extracting data from: {url}")
            url_data, text_data = extract_website_data(url)
            if url_data and text_data:  # Check if data was successfully extracted
                extracted_data.append((url_data, text_data, recipient_email))
            time.sleep(1) # be polite
        else:
            print(f"Skipping invalid URL: {url}")

    save_data_to_csv(extracted_data)


