## ATHENA MAIN FILE ##

# LIBRARIES
import requests
from bs4 import BeautifulSoup
from colorama import Fore
import subprocess
from simple_term_menu import TerminalMenu
import sys
from time import sleep

# VARIABLES

WEB_PAGE = 'https://elpais.com/actualidad/'
OPTIONS = ["El Pais - Actualidad", "Manual"]

# DEFS

def starting_menu(OPTIONS):
    options = OPTIONS
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]

def headlines_menu(headlines):
    options = headlines
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]

def clear():
    subprocess.run('clear', shell=True)

def scrape(web_page):
    # Create an empty dictionary object
    full_list = []
    a_list = []
    href_list = []
    date_list = []

    # Make a GET request to the news website
    response = requests.get(web_page)

    # Extract the HTML content from the response
    html_content = response.text

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all headlines using the appropriate tag and class
    headlines = soup.find_all('h2', class_='c_t')
    for h2_tag in headlines:
        a_tags = h2_tag.find_all("a")
        for a_tag in a_tags:
            href = a_tag.get("href")
            a_list.append(a_tag.text)
            href_list.append(href)

    headlines = soup.find_all('span', class_='c_a_t')
    for span_tag in headlines:
        date_tags = span_tag.find_all("a", id='sc_date')
        for date_tag in date_tags:
            date = date_tag.text
            date_list.append(date)

    full_list.append(a_list)
    full_list.append(href_list)
    full_list.append(date_list)
    full_dict = {}

    for i in range(0, len(a_list)):
        full_dict[a_list[i]] = href_list[i]

    return full_list, full_dict 

def scrape2(web_page):
    # Make a GET request to the news website
    response = requests.get(web_page)

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

    return all_text

def logo():
    print(Fore.RED + '''

 █████╗ ████████╗██╗  ██╗███████╗███╗   ██╗ █████╗ 
██╔══██╗╚══██╔══╝██║  ██║██╔════╝████╗  ██║██╔══██╗
███████║   ██║   ███████║█████╗  ██╔██╗ ██║███████║
██╔══██║   ██║   ██╔══██║██╔══╝  ██║╚██╗██║██╔══██║
██║  ██║   ██║   ██║  ██║███████╗██║ ╚████║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                                   
    ''')
    print(Fore.WHITE + 'Spanish News facility by Tommaso Maria Ungetti\nReleased under GPL Licence - v1.0\n\n')

# MAIN LOGIC

clear()

logo()

opt = starting_menu(OPTIONS)

if opt == 'El Pais - Actualidad':
    clear()
    logo()

    # Populate the 2nd Menu with the articles

    print(Fore.RED + "[SCRAPING THE HTML]", Fore.WHITE + ": Loading articles...")

    try:
        articles, full_dict = scrape(WEB_PAGE)
        print(Fore.GREEN + "[SUCCEDED]", Fore.WHITE + ": Scraping complete")
        sleep(2)
    except:
        print(Fore.RED + "[ERROR]", Fore.WHITE + ": Problem while scraping the web page, check connection or review the code")
        sys.exit(1)
    clear()
    logo()

    # Start 2nd Menu and allow the user to choose the article

    rif = headlines_menu(articles[0])

    full_article = scrape2(full_dict[rif])

    print(full_article)



if opt == 'Manual':
    print('ERROR: Manual not available')
