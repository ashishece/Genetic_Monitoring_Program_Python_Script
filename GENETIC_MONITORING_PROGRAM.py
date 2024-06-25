#!/usr/bin/env python
# coding: utf-8

# In[1]:


cd Desktop


# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


# In[3]:


def search_gene(gene, start_date, num_records):
    # Construct the search query URL
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={gene}+AND+({start_date}[Date+-+Publication]:3000[Date+-+Publication])"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract search results
    articles = soup.find_all('article', class_='full-docsum')

    # Extract titles, abstracts, and URLs of the articles
    results = []
    for article in articles[:num_records]:
        title_element = article.find('a', class_='docsum-title')
        title = title_element.text.strip() if title_element else "Title not found"
        
        article_url_element = article.find('a', class_='docsum-title')
        article_url = "https://pubmed.ncbi.nlm.nih.gov" + article_url_element['href'] if article_url_element else ""
        
        results.append({'Title': title, 'URL': article_url})

    return results


# In[5]:


def main():
    # Ask for the CSV file containing gene list
    csv_file = input("Enter the path to the CSV file containing gene list: ")

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Ask for the number of records to fetch for each gene
    num_records = int(input("Enter the number of records to fetch for each gene: "))

    # Ask for the date after which the records need to be fetched
    start_date = input("Enter the date (YYYY-MM-DD) after which the records need to be fetched: ")

    # Create an empty list to store DataFrames for each gene
    result_dfs = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        gene = row['Gene']

        # Search for the gene within the specified date range
        results = search_gene(gene, start_date, num_records)

        # Create a DataFrame for the current gene's results
        gene_df = pd.DataFrame(results)
        gene_df['Gene'] = gene  # Add gene column
        result_dfs.append(gene_df)

    # Concatenate all DataFrames into a single result DataFrame
    result_df = pd.concat(result_dfs, ignore_index=True)

    # Make URLs clickable
    result_df['URL'] = result_df['URL'].apply(lambda x: f'<a href="{x}">{x}</a>')

    # Save the result DataFrame to an HTML file
    html_output_file = "gene_research_results.html"
    result_df.to_html(html_output_file, index=False, escape=False)
    print(f"HTML results saved to {html_output_file}")


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




