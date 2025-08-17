# Pinterest Content Generator

This script automates the process of generating social media and blog posts from a CSV file of Pinterest trends. It uses the Perplexity.ai API for content generation and stores the results in an Airtable database.

## Features

-   Parses Pinterest Trends CSV data.
-   Generates social media posts using Perplexity.ai.
-   Generates blog posts using Perplexity.ai.
-   Saves the generated content to an Airtable base.

## Prerequisites

Before you run this script, you will need:

-   Python 3
-   A Perplexity.ai API key
-   An Airtable account with an API key, a Base ID, and a Table Name.

## Setup

1.  **Install Dependencies:**

    Open your terminal and run the following command to install the necessary Python libraries:

    ```bash
    pip install pandas perplexipy airtable-python-wrapper
    ```

2.  **Configure the Script:**

    Open the `main.py` file and update the following configuration variables with your own details:

    ```python
    # --- Configuration ---
    PERPLEXITY_API_KEY = "your_perplexity_api_key"
    AIRTABLE_API_KEY = "your_airtable_api_key"
    AIRTABLE_BASE_ID = "your_airtable_base_id"
    AIRTABLE_TABLE_NAME = "your_airtable_table_name"
    ```

3.  **Provide CSV Data:**

    The script currently contains sample CSV data. You can replace the content of the `CSV_DATA` variable in `main.py` with your own Pinterest Trends data.

    ```python
    # --- CSV Data ---
    CSV_DATA = """
    "Your,CSV,Data,Here"
    ...
    """
    ```

4.  **Set up Airtable:**

    Ensure your Airtable table has the following columns (or update the script to match your column names):
    -   `Topic` (Single line text)
    -   `Social Media Post` (Long text)
    -   `Blog Post` (Long text)

## Usage

Once the script is configured, you can run it from your terminal:

```bash
python3 main.py
```

The script will then process each trend in the CSV data, generate the content, and populate your Airtable base. You will see progress updates printed to the console.
