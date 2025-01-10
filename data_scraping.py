import requests
from bs4 import BeautifulSoup
import os
import pandas

#Fetch Met Office Webpage
url = "https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data"
response = requests.get(url)
html_content = response.content

#Content parsing
soup = BeautifulSoup(html_content, 'html.parser') 
table = soup.find('table', class_='table alternate-bg')

#Extract hyperlinks
links = []
for td in table.find_all('td'):
    a_tag = td.find('a', href=True)
    if a_tag:
        links.append(a_tag['href'])
import os

# Create a folder to save the text files
folder_path = 'climate_data_UK(txt)'
os.makedirs(folder_path, exist_ok=True)

# Download and save each text file
for link in links:
    file_name = os.path.join(folder_path, os.path.basename(link))
    file_url = f'{link}'
    file_response = requests.get(file_url)
    with open(file_name, 'wb') as file:
        file.write(file_response.content)

print('Download comlete. Check climate_data_UK folder for text files')