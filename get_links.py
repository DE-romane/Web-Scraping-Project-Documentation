import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import re

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to the ChromeDriver 
service = Service("D:\chromedriver\chromedriver.exe")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the page containing the links
data_links = "https://www.autodoc.co.uk/spares-search?keyword=MAGNETI%20MARELLI"

driver.get(data_links)

# Wait for the span elements with the data-link attribute to load
wait = WebDriverWait(driver, 10)
span_elements = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-link]"))
)

# Extract the links from the data-link attribute and validate the format
links = []
pattern = re.compile(r"https://www\.autodoc\.co\.uk/magneti-marelli/\d+$")  # Regex pattern for desired URL format

for span in span_elements:
    link = span.get_attribute("data-link")
    if link:
        # Parse the link to remove fragments
        parsed_link = urlparse(link)
        clean_link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path
        
        # Check if the clean link matches the desired format
        if pattern.match(clean_link):
            links.append(clean_link)

# Close the browser
driver.quit()

# Remove duplicates
unique_links = list(set(links))

# Create a pandas DataFrame to store the links
df = pd.DataFrame({
    "Links": unique_links
})

# Save the DataFrame to a CSV file
df.to_csv("cleaned_extracted_links.csv", index=False)

print("Links have been cleaned and saved to 'cleaned_extracted_links.csv'.")