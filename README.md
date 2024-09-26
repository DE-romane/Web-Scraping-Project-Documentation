# Web-Scraping-Project-Documentation

## Project Overview

This project involves scraping product data from the website ["https://www.autodoc.co.uk/spares-search?keyword=MAGNETI%20MARELLI"](https://www.autodoc.co.uk/spares-search?keyword=MAGNETI%20MARELLI). The objective is to extract all the product links, clean them, and then gather detailed product data from each link.

### Steps Involved:

### 1. Extract Links from Webpage

The script `get_links.py` is designed to scrape all the links available on the webpage. This includes collecting all links related to product search results.

**Python Script:**
- `get_links.py`

**Tasks:**
- Navigate to the provided URL.
- Scrape all the links available on the page.
- Store these links for further processing.

### 2. Clean the Extracted Links

After extracting all the links, some may not be directly related to individual products. The next step is to clean the list of links, ensuring that only links to product pages are retained.

**Tasks:**
- Remove unnecessary or non-product-related links.
- Save the cleaned list of product links to a CSV file.

**Output:**
- `cleaned_extracted_links.csv`: A CSV file containing only the valid product page links.

### 3. Extract Product Data

The script `get_products_data.py` takes the cleaned list of product links from `cleaned_extracted_links.csv` and scrapes relevant product data from each individual product page.

**Python Script:**
- `get_products_data.py`

**Tasks:**
- Iterate through each product link.
- Extract the following data from each page:
  - `index`: Product index
  - `Link`: The product page URL
  - `Lamp Type`
  - `Voltage [V]`
  - `Rated Power [W]`
  - `Socket Type`
  - `Item number`
  - `Manufacturer`
  - `EAN number`
  - `Condition`
  - `Compatibility`: This is a tree-structured data element, making it ideal for saving in a JSON format rather than a relational table.


### 4. Save Data

The extracted product data is saved in a CSV file.

**Output:**
- `products_data.csv`: A CSV file containing all product data extracted from the links.
