from bs4 import BeautifulSoup
import requests
import json


wiki_page = "https://en.wikipedia.org/wiki/List_of_United_States_stand-up_comedians"

wiki_comics = {}

get_page = requests.get(wiki_page)
page_data = get_page.text
page_soup = BeautifulSoup(page_data, "html.parser")

comedians = page_soup.find_all('div', attrs={'class': 'div-col columns column-width'})
for comic in comedians:
    data = comic.find_all('a')
    for row in data:
        raw_link = row.get('href')
        # remove characters used to handle apostrophes, accents
        cleaned_link = str(raw_link).replace("%27", "'").replace("%C3%A9", "e")
        name = row.get('title')

        # filter unrelated links
        if str(cleaned_link)[:5] == "/wiki" and name is not None and "List " not in name:
            # remove the /wiki/ prefix and also remove any titles ex: (comedian)
            wiki_comics[name.split(" (")[0]] = cleaned_link[6:]
        else:
            pass


""" IMPROV WEBSITE LIST OF COMEDIANS SCRAPE """

imp_url = "https://improv.com/comedians/"

imp_page = requests.get(imp_url)
imp_data = imp_page.text
imp_soup = BeautifulSoup(imp_data, "html.parser")

improv = []

for found_links in imp_soup.find_all('a'):
    link = (found_links.get('href'))
    # all comics have /comic/ prefix and a + between first and last name
    if "/comic/" in str(link):
        stripped = (str(link)
                    .replace("/comic/", "")
                    .replace("/", "")
                    .replace("%22", "")
                    .replace("%27", "")
                    .replace("+", " "))
        # uppercase name for better readability
        name = str(stripped).title()
        improv.append(name)

""" COMPARE DICTS TO BUILD FINAL SCRAPE LIST """

has_wiki = {}
no_wiki = {}

for name in improv:
    if name in wiki_comics:
        has_wiki[name] = wiki_comics[name]
    else:
        no_wiki[name]: "Improv Comic"

# add list of people who have wikipedia entries who didn't show up in pages above
# key is their name, value is the suffix for their wikipedia page url
manuals = {
    'Dc Youngfly': 'Draft:DC_Young_Fly_(2)',
    'Preacher Lawson': 'Preacher_Lawson',
    'Brendan Schaub': 'Brendan_Schaub',
    'Chaunte Wayans': 'Chaunte_Wayans',
    'Colin Kane': 'Colin_Kane',
    'Erik Griffin': 'Erik_Griffin',
    'Felipe Esparza': 'Felipe_Esparza',
    'Ilana Glazer': 'Ilana_Glazer',
    'John Heffron': 'John_Heffron',
    'Marcella Arguello': 'Marcella_Arguello',
    'Michael Blackson': 'Michael_Blackson',
    'Monique': "Mo'Nique",
    'Moses Storm': 'Moses_Storm',
    'Nemr': 'Nemr_Abou_Nassar',
    'Nicole Byer': 'Nicole_Byer',
    'Patti Stanger': 'Patti_Stanger',
    'Rex Navarrete': 'Rex_Navarrete',
    'Sam Morril': 'Sam_Morril',
    'Steve Trevino': 'Steve_Trevino',
    'Tommy Davidson': 'Tommy_Davidson'
}

# duplicate dict of has_wiki, then add manual dict into it for final dict
all_wikis = has_wiki.copy()
all_wikis.update(wiki_comics)
all_wikis.update(manuals)


with open('all_wikis.json', 'w') as fp:
    json.dump(all_wikis, fp)

with open('improv.json', 'w') as fp:
    json.dump(improv, fp)

