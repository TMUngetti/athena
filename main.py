## ATHENA MAIN FILE ##

# LIBRARIES
import requests
from bs4 import BeautifulSoup
from colorama import Fore
import subprocess
from simple_term_menu import TerminalMenu
import sys

# VARIABLES

WEB_PAGE = 'https://elpais.com/actualidad/'
OPTIONS = ["El Pais - Actualidad", "Manual"]

# DEFS

def starting_menu(OPTIONS):
    options = OPTIONS
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

    return full_list    

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
    while True:
        articles = scrape(WEB_PAGE)
        clear()
        logo()
        for i in range(len(articles[0])):
            print(i + 1)
            print(Fore.RED + "[Headline]", Fore.WHITE + f": {articles[0][i]}")
            print(Fore.RED + "[URL]", Fore.WHITE + f": {articles[1][i]}")
            print(Fore.RED + "[Date]", Fore.WHITE + f": {articles[2][i]}\n\n")
            input()
        flag = input("\nRefresh? (y/n): ")

        if flag == "y":
            pass
        elif flag == "n":
            sys.exit(0)
        else:
            print("ERROR: Input not recognized - EXITING WITH CODE 1")
            sys.exit(1)


if opt == 'Manual':
    print('ERROR: Manual not available')
