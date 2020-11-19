import flask
import os
from multiprocessing.dummy import Pool
from .animeX import get_search_result, split_quality, get_anime_episodes, get_download_url, convert_to_object

pool = Pool(2)

app = flask.Flask(__name__)
if not os.environ.get('PRODUCTION'):
    app.config["DEBUG"] = True

API_VERSION = 'v1'
API_ROUTE = f'/api/{API_VERSION}'




@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route(f'{API_ROUTE}/search/', methods=['GET'])
def search():
    if 's' in flask.request.args: keyword = flask.request.args['s']
    else: return "<h1>Invalid parameters sent</h1>"

    results = get_search_result(keyword)
    return flask.jsonify({
        'total': len(results),
        'search-term': keyword,
        'results': results
    })


@app.route(f'{API_ROUTE}/anime/get-links/', methods=['GET'])
def get_links():
    if 'url' in flask.request.args: anime_url = flask.request.args['url']
    else: return "<h1>Invalid parameters sent</h1>"

    # anime_name = flask.request.args.get('anime_title')

    episodes_split = split_quality(get_anime_episodes(anime_url))

    # This is about to get messy
    links_split = {x: pool.map(get_ep_obj, episodes_split[x]) for x in episodes_split if episodes_split[x]}
    # [get_download_url(link) for link in episodes_split[x]]
    # TODO: I'll refactor the above later, just want to see if it works

    return flask.jsonify({
        'anime-url': anime_url,
        'qualities': list(links_split.keys()),
        'data': links_split
    })

# Helper function to nest the 2 for calling
# Don't feel like using lambda
def get_ep_obj(link):
    return convert_to_object(get_download_url(link))
