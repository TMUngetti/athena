import requests
from bs4 import BeautifulSoup

# Make a GET request to the news website
response = requests.get('https://elpais.com/deportes/futbol/2023-12-31/el-arsenal-se-cae.html')

# Extract the HTML content from the response
html_content = response.text

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the <p> tags
p_tags = soup.find_all('p')

# Initialize an empty list to store the text from each <p> tag
text_list = []

# Iterate over the <p> tags and extract the text
for p_tag in p_tags:
    # Remove the text from any child <a> tags using decompose() method
    for a_tag in p_tag.find_all('a'):
        a_tag.decompose()

    # Retrieve the text and append it to the list
    text_list.append(p_tag.get_text())

# Join the text from each <p> tag into one variable
all_text = ' '.join(text_list)

print(all_text)
