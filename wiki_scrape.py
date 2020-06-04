from bs4 import BeautifulSoup
import requests
import wptools
from multiprocessing import cpu_count, Pool
import pandas as pd
import json
from datetime import datetime


with open('all_wikis.json', 'r') as f:
    all_wikis = json.load(f)


def scrape(name):
    bio = {}
    # search each wikipedia page
    try:
        page = wptools.page(all_wikis[name])
        parsed = page.get_parse()

        # if no infobox, pass
        if bool(parsed.data['infobox']) is True:

            # birthdays is main goal, so if none, pass altogether
            try:
                bday_init = parsed.data['infobox']['birth_date']
                bday_raw = bday_init.replace("}", "")
                # bday comes out with words and pipes -- separate on pipes, keep dates, rejoin and clean
                bday_nums = [str(x) for x in bday_raw.split("|") if x.isdigit()]
                # check if formatted as date
                if len(bday_nums) > 0:
                    bday = ('-').join(bday_nums)
                    bio['scraped_bday'] = bday
                # check if formatted as written out string (eg. March 1, 1980)
                else:
                    try:
                        bday_split = bday_raw.split("|")
                        for bday_part in bday_split:
                            try:
                                bday_stp = datetime.strptime(bday_part, "%B %d, %Y")
                                bio['scraped_bday'] =bday_stp
                            except:
                                pass
                    except:
                        bio['scraped_bday'] = ""


                # hometown
                try:
                    home_town = parsed.data['infobox']['birth_place']
                    home_town = home_town.replace('[', '').replace(']', '')
                    bio['home_town'] = home_town
                except KeyError:
                    bio['home_town'] = "No home town"

                # deceased info
                try:
                    passed_away = parsed.data['infobox']['death_date']
                    # split on pipes, keep year/month/day
                    death_date_raw = passed_away.split("|")[1:4]
                    death_date = ('-').join(death_date_raw)
                    living_status = "Deceased"
                    bio['scraped_dday'] = death_date
                    bio['living_status'] = living_status
                except KeyError:
                    living_status = "Alive"
                    bio['scraped_dday'] = ""
                    bio['living_status'] = living_status

                # try to pull first paragraph with info on comic
                try:
                    page = requests.get('http://en.wikipedia.org/wiki/' + all_wikis[name])
                    data = page.text

                    soup = BeautifulSoup(data, "html.parser")

                    paragraphs = soup.find_all('p')
                    sentences = ""

                    for par in paragraphs:
                        sentences += par.text

                    sentences = sentences.replace("\n", "")
                    bio['summary'] = '.'.join(sentences.split('.')[:4]) + '.'

                except:
                    bio['summary'] = "No summary available."

                # add wiki page url, wiki image
                try:
                    bio['wiki_page'] = "https://en.wikipedia.org/wiki/" + all_wikis[name]
                except:
                    bio['wiki_page'] = "No link"

                try:
                    image = parsed.images(['url'])[0]['url']
                    bio['image'] = image
                except:
                    bio['image'] = "No Image"

            # no birthday in infobox
            except KeyError:
                pass

        # no infobox
        else:
            pass

    # not found in wikipedia
    except LookupError:
        pass

    return name, bio


if __name__ == '__main__':
    pool = Pool(cpu_count())
    bios = dict(pool.map(func=scrape, iterable=all_wikis))
    pool.close()
    pool.join()
    df = pd.DataFrame.from_dict(bios, orient='index')
    df_clean = df.loc[df['scraped_bday'] != ""]
    df_clean.to_csv('wiki_data.csv')
