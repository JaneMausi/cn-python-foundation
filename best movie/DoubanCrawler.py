from expanddouban import getHtml
from bs4 import BeautifulSoup
import csv

category_list = ["剧情", "喜剧", "动作", "爱情", "科幻", "悬疑", "惊悚",
                 "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史",
                 "战争", "西部", "奇幻", "冒险", "灾难", "武侠", "情色"]
location_list = ["中国大陆", "美国", "香港", "台湾", "日本", "韩国", "英国",
                 "法国", "德国", "意大利", "西班牙", "印度", "泰国", "俄罗斯",
                 "伊朗", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]


class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def get_movie_info(self):
        return [self.name, self.rate, self.location, self.category,
                     self.info_link, self.cover_link]


# get movie url selected by category and location
def getMovieUrl(category, location):
    url_body = "https://movie.douban.com/tag/#/"
    url_tags = ','.join(["电影", item_category, item_location])
    url_attr = '&'.join(["sort=S", "range=9,10", "tags={}".format(url_tags)])
    movie_url = url_body + "?" + url_attr
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
        m = Movie(information.find(class_='title').text, information.find(class_='rate').text,
                  location, category, item.get('href'), cover.get('src'))
        movies.append(m)
    return movies


if __name__ == "__main__":
    # get movies
    movie_dict = {}
    for item_category in ["剧情", "喜剧", "动作"]:
        for item_location in location_list:
            if item_category not in movie_dict:
                movie_dict[item_category] = getMovies(item_category, item_location)
            else:
                movie_dict[item_category].extend(getMovies(item_category, item_location))
    # create movies.csv
    with open('movies.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='&')
        for key in movie_dict:
            for movie in movie_dict[key]:
                writer.writerow(movie.get_movie_info())
    # analyze
    statistics = {}
    statistics_reverse = {}
    output = ''
    for category in movie_dict:
        movie_list = movie_dict[category]
        statistics['all'] = len(movie_list)
        for movie in movie_list:
            if movie.location not in statistics:
                statistics[movie.location] = 0
            else:
                statistics[movie.location] += 1

        statistics_reverse = {value:key for key, value in statistics.items()}
        rank = sorted(statistics.values(), reverse=True)
        if len(rank) < 4:
            exit(1)

        output = output + "类别: {}\n" \
                          "排名前三地区: {}, {}, {}\n" \
                          "分别占比: {} {}, {} {}, {} {}\n\n\n".format(category,
                                                                   statistics_reverse[rank[1]],
                                                                   statistics_reverse[rank[2]],
                                                                   statistics_reverse[rank[3]],
                                                                   statistics_reverse[rank[1]],
                                                                   format(float(rank[1])/float(rank[0]) * 100, '.2f'),
                                                                   statistics_reverse[rank[2]],
                                                                   format(float(rank[2])/float(rank[0]) * 100, '.2f'),
                                                                   statistics_reverse[rank[3]],
                                                                   format(float(rank[3])/float(rank[0]) * 100, '.2f'))

        # create output.txt
        with open('output.txt', 'w') as f:
            f.write(output)
