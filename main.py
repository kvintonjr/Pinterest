import os
import io
import pandas as pd
from perplexipy import PerplexityClient
from airtable import Airtable

# --- Configuration ---
PERPLEXITY_API_KEY = "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"
AIRTABLE_API_KEY = "pat0zCr6ASv1lvhzF.f97e6342cdbc420753dae266f97f1c861b9ff101d03aeaa5b1fa21bf0f0c1e31"
AIRTABLE_BASE_ID = "app9iR4y0YS3b3e4N"
AIRTABLE_TABLE_NAME = "Echoes_of_Now_Table"

# --- CSV Data ---
CSV_DATA = """
"Pinterest Trends tool – https://trends.pinterest.com/"
Selected Filters
Trends Type,Growing trends
Date Range,90 days before 2025-08-04
Interests,"All"
Include keywords,"All"
Age,"All"
Gender,"All"

,,,,,Data in the date columns reflects the normalized search volume for this trend type
Rank,Trend,Weekly change,Monthly change,Yearly change,2025-05-12,2025-05-19,2025-05-26,2025-06-02,2025-06-09,2025-06-16,2025-06-23,2025-06-30,2025-07-07,2025-07-14,2025-07-21,2025-07-28,2025-08-04
1,back to school outfits,"10%","300%","3%",2,3,5,7,10,15,20,28,44,70,79,89,100
2,first day of school outfit,"50%","200%","40%",4,5,7,10,12,18,18,22,32,61,55,68,100
3,back to school nails,"40%","500%","50%",1,1,1,2,3,8,7,11,25,33,49,70,100
4,fall outfits,"30%","400%","10%",6,7,10,8,8,12,14,18,28,46,59,77,100
5,back to school,"20%","200%","40%",4,6,8,10,13,19,23,30,48,91,77,85,100
6,malachi barton,"-1%","1,000%","500%",5,6,8,8,7,7,7,7,9,56,92,100,98
7,home garden ideas,"100%","-20%","10,000%+",0,44,16,17,25,22,100,66,10,14,37,38,77
8,back to school hairstyles,"7%","200%","10%",2,3,5,8,10,17,23,35,62,74,86,93,100
9,zucchini bread,"1%","200%","4%",12,14,16,17,22,28,33,41,49,74,95,98,100
10,rumi,"-5%","200%","3,000%",2,2,1,1,2,1,16,59,71,93,100,100,94
"""

def main():
    """
    Main function to process Pinterest trends, generate content, and save to Airtable.
    """
    # --- 1. Parse CSV data ---
    # The CSV data has a variable-length header. We need to find where the
    # actual data starts. The data starts with the line "Rank,Trend,..."
    lines = CSV_DATA.strip().split('\n')
    start_index = -1
    for i, line in enumerate(lines):
        if line.startswith('Rank,Trend,'):
            start_index = i
            break

    if start_index == -1:
        raise ValueError("Could not find the start of the data in the CSV.")

    # Rejoin the lines from the start of the data and read into pandas
    csv_from_data = "\n".join(lines[start_index:])
    data_io = io.StringIO(csv_from_data)
    trends_df = pd.read_csv(data_io)

    # --- 2. Initialize clients ---
    perplexity_client = PerplexityClient(key=PERPLEXITY_API_KEY)
    airtable_client = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)

    # --- 3. Process each trend ---
    for index, row in trends_df.iterrows():
        trend = row['Trend']
        print(f"Processing trend: {trend}")

        try:
            # --- Generate Social Media Post ---
            social_media_prompt = f"You are a creative social media manager. Generate a short, engaging social media post about the trending topic: '{trend}'. Include relevant hashtags."
            social_media_post = perplexity_client.query(social_media_prompt)
            print(f"  - Generated social media post.")

            # --- Generate Blog Post ---
            blog_post_prompt = f"You are a helpful and informative blog writer. Write a short blog post (around 200 words) about the trending topic: '{trend}'. The tone should be informative and engaging for a general audience."
            blog_post = perplexity_client.query(blog_post_prompt)
            print(f"  - Generated blog post.")

            # --- Save to Airtable ---
            # Assuming Airtable has columns: 'Topic', 'Social Media Post', 'Blog Post'
            record = {
                'Topic': trend,
                'Social Media Post': social_media_post,
                'Blog Post': blog_post
            }
            airtable_client.insert(record)
            print(f"  - Saved to Airtable.")

        except Exception as e:
            print(f"An error occurred while processing trend '{trend}': {e}")

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
