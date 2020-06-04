import time
from bs4 import BeautifulSoup
import requests
import json

# words that must be included in title
search_words = ['netflix', 'special', 'stand', 'stand-up', 'hbo', 'hulu', 'amazon', 'showtime', 'tour']

search_names = {}

with open('all_wikis.json', 'r') as f:
    all_wikis = json.load(f)


for key, value in all_wikis.items():
    search_names[key] = value.replace("_", "+")

news = {}

# for log
search_count = 1

for key, value in search_names.items():

    # show name, number for each person to monitor progress
    print(key, search_count)

    page = requests.get("https://www.google.com/search?q="
                        + value +
                        "+special&btnG=Search&biw=1600&bih=757&gbv=1&tbs=qdr%3Aw&tbm=nws")

    while page.status_code == 200:
        data = page.text
        soup = BeautifulSoup(data, "html.parser")

        top5 = soup.find_all("div", class_='BNeawe vvjwJb AP7Wnd')[:5]
        post_times_raw = soup.find_all('span', class_='r0bn4c rQMQod')[:10:2]

        # get date/time posted
        posted_time = []
        for time_text in post_times_raw:
            posted_time.append(time_text.text)

        # get summary text preview
        text_preview = []
        for post in post_times_raw:
            preview = (post.next_sibling.next_sibling)
            text_preview.append(preview)

        # get urls to articles
        links_with_dupes = []

        # ignore all google's standard links for layout
        for link in soup.select('a[href*="url"]'):
            links_with_dupes.append(link.get('href'))

        # keep first 5 links, skipping dupes
        links = links_with_dupes[:10:2]

        news[key] = {}

        for index, title in enumerate(top5):

            title_words = [word.lower() for word in title.text.split(' ')]

            # to avoid noise, want person's name and at least one of the search keywords in the article title
            if key in title.text:
                if (len(set(title_words).intersection(search_words))) > 1:
                    # check if dict is empty -- if so, try to fill, otherwise pass so no multiple stories per person
                    if bool(news[key]) is False:
                        try:
                            news[key]['title'] = title.text
                            news[key]['body'] = text_preview[index]
                            news[key]['date'] = posted_time[index]
                            news[key]['link'] = "google.com" + links[index]
                        except:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        break
    else:
        print(key, page.status_code)
        break

    # to avoid making google mad
    time.sleep(6)

    search_count += 1


def drop_no_news(a_dict):
    new_dict = {}
    for k, v in a_dict.items():
        if isinstance(v, dict):
            v = drop_no_news(v)
        if v is not None:
            new_dict[k] = v
    return new_dict or None

# remove all people who had no news stories
final_news = drop_no_news(news)

with open('news_dump.json', 'w') as fp:
    json.dump(final_news, fp)


