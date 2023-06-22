import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, request , render_template
import requests



def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
#url = "https://www.epa.gov/risk/regional-screening-levels-rsls-generic-tables"  # Replace with your desired URL
def get_url(url):
    html_content = get_html_content(url)

    if html_content is not None:
        # Store the HTML content in a variable instead of printing
        html_variable = html_content
        #print(html_variable)

    soup = BeautifulSoup(html_variable, 'html.parser')

    # Find the table tag
    table_tag = soup.find_all('table')
    # print(table_tag)

    # Extract the table tag as a string

    table_html = str(table_tag)
    # print(table_html)

    dfs = pd.read_html(table_html)

    i = 1

    for x in dfs:
        print(type(x))
        print("----------------------------")


        x.to_csv("table"+str(i)+".csv",index=False)
        i+=1



