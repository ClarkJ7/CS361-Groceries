import requests
from bs4 import BeautifulSoup, Comment
import re


def get_recipes():
    url = "https://en.wikibooks.org/wiki/Cookbook:Recipes"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    element = soup.find("h2")

    recipe_list = []

    stop = False

    while stop is False:
        if element.name == 'ul':
            for a in element.find_all('a'):
                recipe = {}
                recipe["link"] = format_link(a['href'])
                recipe["name"] = a.get_text()
                recipe_list.append(recipe)

                if recipe["name"] == "Zuppa Toscana":
                    stop = True

        element = element.next_sibling

    return recipe_list


def format_link(raw_link):
    colon_index = re.search("Cookbook:", raw_link)
    formatted_link = raw_link[colon_index.end():]
    return formatted_link
