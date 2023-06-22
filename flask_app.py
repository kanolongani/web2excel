import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, send_from_directory
import os 

def get_html_content(url):
    try:
        print(url)
        head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        response = requests.get(url , headers= head)
        print(response.status_code)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
        return response.text
    
    except requests.exceptions.RequestException as e:
        if '403' in str(e):
            # Handle the '403' error here
            print("Forbidden error (403) occurred.")
            # Return None to indicate the error
            return None
        else:
            # Handle other RequestException errors
            print(f"An error occurred: {e}")
            return None
    
def get_url(url):
    html_content = get_html_content(url)

    if html_content is not None:
        # Store the HTML content in a variable instead of printing
        html_variable = html_content

    soup = BeautifulSoup(html_variable, 'html.parser')

    # Find the table tag
    table_tag = soup.find_all('table')

    if table_tag == []:

        return None

    # Extract the table tag as a string
    table_html = str(table_tag)

    dfs = pd.read_html(table_html)

    i = 1
    file_paths = []

    for df in dfs:
        file_path = f"table{i}.xlsx"
        try:
            df.to_excel(file_path, index=False)
        except:
            df.to_excel(file_path)

        file_paths.append(file_path)
        i += 1
    print(len(file_paths))
    return file_paths

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_file/<path:filename>')
def download_file(filename):
    directory = os.getcwd()  # Get current working directory
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/preview_file/<path:filename>')
def preview_file(filename):
    df = pd.read_excel(filename)  # Read the Excel file
    html_table = df.to_html(index=False)  # Convert the DataFrame to HTML table

    table_name = os.path.splitext(filename)[0]  # Extract the table name from the filename

    return render_template('preview.html', table=html_table, table_name=table_name)

@app.route('/process_url', methods=['POST', 'GET'])
def process_url():
    url = request.form.get('url')
    print(url)
    file_paths = []  # Initialize file_paths variable

    html_content = get_html_content(url)

    

    if html_content is None:
        # Display the 403 error on the webpage
        return render_template('403.html', generated=False, error="Forbidden error (403) occurred.")

    # Rest of the code to process the URL and generate Excel files
    file_paths = get_url(url)  # Update file_paths variable

    if file_paths is None:
        return render_template('tablerror.html', generated=False, error="Forbidden error (403) occurred.")


    return render_template('index.html', generated=True, file_paths=file_paths)
    # return "test"

if __name__ == '__main__':
    app.run(host = '0.0.0.0' , debug=True , port=80)
