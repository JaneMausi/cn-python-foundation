from expanddouban import getHtml
from bs4 import BeautifulSoup
import csv


class Movie:
    def __init__(self, info):
        self.name = info[0]
        self.rate = info[1]
        self.location = info[2]
        self.category = info[3]
        self.info_link = info[4]
        self.cover_link = info[5]

    def get_movie_info(self):
        return [self.name, self.rate, self.location, self.category,
                     self.info_link, self.cover_link]


# get movie url selected by category and location
def getMovieUrl(category=None, location=None):
    url_body = "https://movie.douban.com/tag/#/"
    if category is not None and location is not None:
        url_tags = ','.join(["电影", item_category, item_location])
        url_attr = '&'.join(["sort=S", "range=9,10", "tags={}".format(url_tags)])
        movie_url = url_body + "?" + url_attr
    else:
        movie_url = url_body + "?" + '&'.join(["sort=S", "range=9,10", "tags=电影"])
    return movie_url


# input is html text, output is dictionary of a movie's information
def getMovies(category, location):
    movies = []
    url = getMovieUrl(category, location)
    html = getHtml(url, loadmore=True)
    soup = BeautifulSoup(html, 'html.parser')
    alist = soup.find(id='wrapper').find(class_='list-wp').find_all('a')
    for item in alist:
        cover = item.find(class_='cover-wp').find(class_='pic').img
        information = item.p
        m = Movie([information.find(class_='title').text, information.find(class_='rate').text,
                  location, category, item.get('href'), cover.get('src')])
        movies.append(m)
    return movies


def get_location_tags():
    url = getMovieUrl()
    html = getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find(id='wrapper').find(class_='tags').find_all(class_='category')[2].find_all(class_='tag')
    categories = []
    for item in tags[1:]:
        categories.append(item.text)
    return categories


if __name__ == "__main__":
    location_list = get_location_tags()
    # get movie list
    movie_dict = {}
    for item_category in ["剧情", "喜剧", "奇幻"]:
        for item_location in location_list:
            if item_category not in movie_dict:
                movie_dict[item_category] = getMovies(item_category, item_location)
            else:
                movie_dict[item_category].extend(getMovies(item_category, item_location))
    # create movies.csv
    with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='&')
        for key in movie_dict:
            for movie in movie_dict[key]:
                writer.writerow(movie.get_movie_info())
    # debug
    '''
    movie_dict = {}
    with open('movies.csv', 'r', encoding='utf-8') as csvfile:
        for line in csvfile:
            info = line.strip('\n').split('&')
            m = Movie(info)
            if info[3] not in movie_dict:
                movie_dict[info[3]] = []
                movie_dict[info[3]].append(m)
            else:
                movie_dict[info[3]].append(m)
    '''
    # analyze
    output = ''
    for category in movie_dict:
        statistics = {}
        movie_list = movie_dict[category]
        statistics['all'] = len(movie_list)
        for movie in movie_list:
            if movie.location not in statistics:
                statistics[movie.location] = 1
            else:
                statistics[movie.location] += 1
        # when there is no movie in this category
        if 0 == len(statistics):
            output = output + "\n\n类别: {}\n该类别无电影资源\n".format(category)
            continue
        #
        re_stat = {value:key for key, value in statistics.items()}
        rank = sorted(statistics.values(), reverse=True)
        output = output + "\n\n类别: {}\n电影数量排名前列地区: \n".format(category)
        for i in range(len(rank)):
            if 0 == i:
                continue
            if i > 3:
                break
            output = output + \
                     "  {} {}\n".format(re_stat[rank[i]], format(float(rank[i])/float(rank[0]) * 100, '.2f'))
        # create output.txt
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(output)
