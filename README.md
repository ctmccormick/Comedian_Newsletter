# Comedian_Newsletter

## Purpose
This newsletter was created to help employees at the Hollywood Improv stay up to date on birthdays, death anniversaries, and news articles for stand-up comedians.

## File Summaries

### get_comedians.py
Scrape Wikipedia's page of US Stand Up Comedians and Improv.com to get list of comedians names and Wikipedia urls.

Outputs:

all_wikis.json

improv.json


### wiki_scrape.py
Use Wikipedia's API, wptools, to pull biographical information on each comic from their infobox.  Also uses `requests` and `BeautifulSoup` to pull the first two sentences of each comic's summary.

Outputs:

wiki_data.csv


### news_scrape.py
Scrapes Google News for recent news stories about each comic.

Outputs:

news_dump.json


### df_clean.py
Merges manual lookups with scraped bio data.  Cleans dates and names, and calculates ages.

Outputs:

wiki_data_ddays.json
wiki_data_bdays.json


### email_send.py
Creates HTML based on all relevant birthdays, death anniversaries, and news stories.  Handles MS Outlook formatting issues when needed, and sends an email to daily recipients and weekly recipients.


### update_web_files.py
Uses `selenium` to update the files on the hosted website that people can visit if they are unable to view the email locally.


### newsletter_dag.py
Airflow dag to manage the process on a daily basis.  

get_comedians >> wiki_scrape >> news_scrape >> df_clean >> [email_send, update_web_files]


## Packages used
    pandas
    bs4
    wptools
    requests
    multiprocessing
    selenium
    airflow
    smtplib
    email
    collections
    time
    datetime
    json
    
