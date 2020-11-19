import requests, re

API = 'https://animepahe.com/api'
KWIK_HEADER = {'referer': 'https://kwik.cx'}
s = requests.Session()

def query_api(params):
    response = requests.get(API, params=params).json()
    total = response.get('total')
    data = response.get('data')
    return total, data


def search(search_term):
    # form the API query
    params = {'m': 'search', 'l': '10', 'q': search_term}
    # get the data
    return query_api(params)


def get_episodes(anime_id):
    # form the API query again
    params = {'m': 'release', 'id': str(anime_id), 'l': '-1', 'sort': 'episode_desc', 'page': '1'}
    # get the data again
    return query_api(params)


def get_embed_links(episode_id):
    params = {'m': 'embed', 'id': str(episode_id), 'p': 'kwik'}
    qualities = ['480p', '720p', '1080p']
    embeds = query_api(params)[1]
    for q in qualities:
        if embeds[str(episode_id)].get(q):
            return embeds[str(episode_id)].get(q)['url']
    return 
    

def get_token(kwik_link):
    res = s.get(kwik_link, headers=KWIK_HEADER).text
    token = re.search(r'name="_token" value="(\w+)"', res).group(1)
    return token


def get_down_link(embed_link):
    kwik_link = re.sub('kwik.cx/e/', 'kwik.cx/f/', embed_link)
    form_action = re.sub('kwik.cx/e/', 'kwik.cx/d/', embed_link)
    form_data = {'_token': get_token(kwik_link)}
    down_link = s.post(form_action, data=form_data, headers={'referer': kwik_link}, allow_redirects=False).headers.get('location')
    return down_link
