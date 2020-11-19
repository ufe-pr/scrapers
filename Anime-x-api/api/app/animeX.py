import requests
import re
from bs4 import BeautifulSoup


# Helper method to create a dict for episodes
# indicating their episode numbers and anime they belong to
def convert_to_object(episode_url, anime_title='Unknown', quality=''):
    episode_num_str = re.search(r"(?<=\s)[\d-]{2}(?=\s)", episode_url)
    episode_num = episode_num_str.group() if episode_num_str else 'UN'

    return {
        'number': episode_num,
        'quality': quality,
        'url': episode_url,
        # 'title': anime_title,
    }


def get_search_result(search_item):
    # search for a given anime
    search_url = "https://www.animeout.xyz/"
    params = {
        "s": search_item
    }
    r = requests.get(search_url, params=params)
    search_result_html = BeautifulSoup(r.text, "html.parser")

    search_result = []
    for i in search_result_html.findAll("article", {"class": "post-item"}):
        try:
            search_result.append({
                "name": i.find("h3").text,
                "url": i.find("a")["href"],
                "img_url": i.find("img")["src"]
            })
        except:
            print(i)
    return search_result


def split_quality(episodes: list):
    # Create a dictionary for holding the different lists
    # This most likely isn't efficient since there might be
    # cases where the quality name doesn't match my specs
    # so I'll add an unsorted to the dictionary
    qualities = ['480p', '720p', '1080p']
    sorts = {i: [] for i in qualities }
    sorts['unsorted'] = []

    # Loop through the episodes and sort them accordingly
    for episode in episodes:
        for quality in qualities:
            if quality in episode:
                sorts[quality].append(episode)
                break
        else:
            sorts['unsorted'].append(episode)

    # TODO: Remove un-needed keys from dictionary
    
    # Return the split data
    return sorts


def get_anime_episodes(anime_url):
    # get the episodes in the anime by parsing all links that are videos
    r = requests.get(anime_url)
    anime_result = BeautifulSoup(r.text, "html.parser")

    episodes = []
    for i in anime_result.findAll("a"):
        try:
            if i["href"][-3:] in ["mkv", "mp4]"]:
                episodes.append(i["href"])
        except:
            pass
    return episodes


def get_download_url(anime_url):
    # get the video download URL
    r = requests.get(anime_url)
    pre_download_page = BeautifulSoup(r.text, "html.parser")
    pre_download_url = pre_download_page.find("a", {"class": "btn"})["href"]

    r = requests.get(pre_download_url)
    download_page = BeautifulSoup(r.text, "html.parser")
    # using a try catch because .text returned empty on some OS
    try:
        download_url = download_page.find(
            "script", {"src": None}).text.split('"')[1]
    except:
        download_url = download_page.find(
            "script", {"src": None}).contents[0].split('"')[1]
    return download_url


def check_update():
    # check if there's a higher version of the app
    commit_count = 29
    repo_commit_count = len(requests.get(
        "https://api.github.com/repos/LordGhostX/animeX-v2/commits").json())
    if commit_count != repo_commit_count:
        print("\nYou are using an outdated version of animeX. Please update from "
              "https://github.com/LordGhostX/animeX-v2")
    else:
        print("\nYou're ready to go :)")

