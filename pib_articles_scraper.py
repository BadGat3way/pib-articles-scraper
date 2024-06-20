import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def articles_compiler(day_value, month_value, year_value, session):
    mapping = {}
    base_url = "https://pib.gov.in/AllRelease.aspx"

    response = session.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    viewstate = soup.find(id="__VIEWSTATE")['value']
    eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
    viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']

    ministry_value = "0"  # All Ministry - index of the ministry in the dropdown
    payload = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$ddlMinistry",
        "__EVENTARGUMENT": "",
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "__VIEWSTATEENCRYPTED": "",
        "__LASTFOCUS": "",
        "ctl00$Bar1$ddlregion": "3",
        "ctl00$Bar1$ddlLang": "1",
        "ctl00$ContentPlaceHolder1$ddlMinistry": ministry_value,
        "ctl00$ContentPlaceHolder1$ddlday": day_value,
        "ctl00$ContentPlaceHolder1$ddlMonth": month_value,
        "ctl00$ContentPlaceHolder1$ddlYear": year_value,
    }

    response = session.post(base_url, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')

    releases = soup.find_all('div', {'class': 'content-area'})
    releases = releases[0].find_all('ul')[0]

    for child in releases.children:
        if child.name == 'li':    # child.text = Headline of article
            mapping[child.text] = urljoin(base_url, child.a['href']).replace("ReleseDetail", "ReleasePage")
    return mapping

def fetch_article(link, session):
    response = session.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    all_span = soup.find_all("span")
    article_content = ""
    for ch in all_span:
        if ch.string is not None and ch.string not in article_content:
            article_content += ch.string
    return article_content.strip()

def write_to_csv(rows):
    with open('pib_articles.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def main():
    with open('pib_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date of Publication", "Headline", "Article Content", "Article Link"])

    session = requests.Session()
    date_range = pd.date_range(start='1/1/2024', end='3/31/2024')

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_date = {executor.submit(articles_compiler, date.day, date.month, date.year, session): date for date in date_range}
        for future in as_completed(future_to_date):
            date = future_to_date[future]
            try:
                article_map = future.result()
                future_to_article = {executor.submit(fetch_article, link, session): (link, headline) for headline, link in article_map.items()}
                rows = []
                for article_future in as_completed(future_to_article):
                    link, headline = future_to_article[article_future]
                    try:
                        article_content = article_future.result()
                        rows.append([date.date(), headline, article_content, link])
                    except Exception as exc:
                        print(f'Error fetching article content from {link}: {exc}')
                write_to_csv(rows)
            except Exception as exc:
                print(f'Error fetching articles for {date}: {exc}')

if __name__ == '__main__':
    main()
