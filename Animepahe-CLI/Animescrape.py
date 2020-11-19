from functions import search, get_down_link, get_embed_links, get_episodes
import os
try:
    os.mkdir(os.path.join('links'))
except:
    pass


def main():

    print('Welcome y\'all...\n', '-'*15, sep='')

    search_term = input('What\'s ur search term: ')
    total, results = search(search_term)

    print('\nThe top {} matches are:\n'.format(total))

    for i, anime in enumerate(results, start=1):
        print('{}.\t{}'.format(i, anime.get('title')))

    anime = results[int(input('Enter ur anime number: ')) - 1]

    file_path = os.path.join('links', anime['slug'] + '.txt')
    print('There are {} episodes for this anime'.format(anime['episodes']))
    print('Download links will be saved in {}'.format(file_path))

    episodes = get_episodes(anime['id'])[1]
    episodes.reverse()

    with open(file_path, 'w') as f:
        for i, episode in enumerate(episodes, 1):
            print('Getting link for episode', i)
            embed_link = get_embed_links(episode['id'])
            down_link = get_down_link(embed_link)
            f.write(down_link + '\n ')
            print('Got link for episode', i)

        f.close()

    print('That\'ll be all... Thank you :D')


if __name__ == '__main__':
    main()
