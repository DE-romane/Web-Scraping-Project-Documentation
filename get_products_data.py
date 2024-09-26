import csv
import os
import pandas as pd  # Import pandas to work with DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

# Set up Selenium WebDriver
service = Service('D:/chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# File containing the URLs to process
input_csv_file = 'cleaned_extracted_links.csv'  

# Output CSV file to save scraped data
output_csv_file = 'products_data.csv'

# Create an empty DataFrame with the specified columns
columns = ['index', 'Link', 'Lamp Type', 'Voltage [V]', 'Rated Power [W]', 'Socket Type', 'Item number', 'Manufacturer', 'EAN number', 'Condition', 'Compatibility']
df = pd.DataFrame(columns=columns)

# Open the input CSV file to read URLs
with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    url_reader = csv.reader(infile)

    # Read through each row (which contains a URL) in the input CSV
    for index, row in enumerate(url_reader, start=1):
        website_url = row[0].strip()  # Assuming the URL is the only entry in the row
        print(f"Processing URL {index}: {website_url}")

        # Load the dynamic webpage for each URL
        driver.get(website_url)

        # Increase the wait time to handle slower page loading
        wait = WebDriverWait(driver, 100)

        try:
            # Ensure the collapsible content is loaded
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-info-block__wrap")))

            # Use JavaScript to expand all collapsible sections
            accordion_sections = driver.find_elements(By.CLASS_NAME, 'product-info-block__item-title')
            for section in accordion_sections:
                driver.execute_script("arguments[0].click();", section)

            # Allow time for the content to expand after JavaScript click
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-info-block__item-list')))

            # Get the HTML content of the page
            html_content = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract product data from the table-like structure
            table_data = {}
            for item in soup.find_all('li', class_='product-description__item'):
                title = item.find('span', class_='product-description__item-title').text.strip()
                value = item.find('span', class_='product-description__item-value').text.strip()
                table_data[title.rstrip(':')] = value

            # Prepare row data based on expected columns (fill missing values with empty strings)
            row_data = {
                'index': index,
                'Link': website_url,
                'Lamp Type': table_data.get('Lamp Type', ''),
                'Voltage [V]': table_data.get('Voltage [V]', ''),
                'Rated Power [W]': table_data.get('Rated Power [W]', ''),
                'Socket Type': table_data.get('Socket Type', ''),
                'Item number': table_data.get('Item number', ''),
                'Manufacturer': table_data.get('Manufacturer', ''),
                'EAN number': table_data.get('EAN number', ''),
                'Condition': table_data.get('Condition', '')
            }

            # Extract compatibility data 
            compatibility_data = []
            compatibility_section = soup.find_all('div', class_='product-info-block__item')

            for section in compatibility_section:
                manufacturer_tag = section.find('a', class_='product-info-block__item-title')

                # Check if manufacturer_tag exists before trying to extract text
                if manufacturer_tag:
                    manufacturer = manufacturer_tag.text.strip()
                    models_list = section.find('ul', class_='product-info-block__item-list')

                    if models_list:
                        models = []
                        # Find all model titles under each manufacturer
                        for model_title in models_list.find_all('span', class_='product-info-block__item-list__title'):
                            models.append(model_title.text.strip())

                        # Extract the models from the sublist within the manufacturer
                        for model_sublist in models_list.find_all('ul', class_='product-info-block__item-sublist'):
                            for model in model_sublist.find_all('li'):
                                models.append(model.text.strip())

                        # Add compatibility data for the manufacturer
                        compatibility_data.append(f"{manufacturer}: " + ", ".join(models))
                else:
                    print(f"Manufacturer not found for URL {website_url}")

            # Join all compatibility data into a single string
            row_data['Compatibility'] = " | ".join(compatibility_data)

        except TimeoutException:
            print(f"Element with class name 'product-info-block__wrap' not found for URL {website_url}, continuing to next URL.")
            # Prepare row data with empty values for missing elements
            row_data = {
                'index': index,
                'Link': website_url,
                'Lamp Type': '',
                'Voltage [V]': '',
                'Rated Power [W]': '',
                'Socket Type': '',
                'Item number': '',
                'Manufacturer': '',
                'EAN number': '',
                'Condition': '',
                'Compatibility': ''
            }

        # Create a DataFrame from the row data and concatenate it to the existing DataFrame
        new_row_df = pd.DataFrame([row_data])
        df = pd.concat([df, new_row_df], ignore_index=True)

# Save the DataFrame to a CSV file
df.to_csv(output_csv_file, index=False, encoding='utf-8')

# Close the driver after processing all URLs
driver.quit()

print(f"Data from all URLs saved to {output_csv_file}")