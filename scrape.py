import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search_bbc(topic):
    api_key = "9ce583b29831a032f0a8cb5283857159d3f99833cdc9675ffa20f007c52c6769"

    params = {
      "engine": "google",
      "q": f"site:bbc.com {topic}",
      "api_key": api_key,
      "num": 10
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    articles = []
    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if 'bbc.com' in link and '/news/' in link:
                articles.append(link)

    return list(set(articles))

def search_cnn(topic):
    api_key = "9ce583b29831a032f0a8cb5283857159d3f99833cdc9675ffa20f007c52c6769"

    params = {
      "engine": "google",
      "q": f"site:cnn.com {topic}",
      "api_key": api_key,
      "num": 10
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    articles = []
    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if 'cnn.com' in link:
                articles.append(link)

    return list(set(articles))

def search_fox(topic):
    query = '+'.join(topic.split())
    url = f'https://www.foxnews.com/search-results/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/news/' in href or '/politics/' in href:
            full_url = href if href.startswith('http') else 'https://www.foxnews.com' + href
            articles.append(full_url)
    return list(set(articles))

def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article = ' '.join([p.text for p in paragraphs])
    return article

def get_article_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.title:
            return soup.title.text.strip()
        else:
            return "No Title"
    except:
        return "No Title"