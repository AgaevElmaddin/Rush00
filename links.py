from re import S
import requests
from bs4 import BeautifulSoup

class Links:
    """
    Analyzing data from links.csv
    """
    first_line_list = ["movieId","imdbId","tmdbId"]
    limit_films = 5
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        f = open(path_to_the_file + "links.csv", "r")
        self.movieId = list()
        self.imdbId = list()
        self.tmdbId = list()
        first_line = True
        elem_count = len(self.first_line_list)
        for line in f:
            if first_line:
                word_list = line[0:-1].split(",")
                if word_list != self.first_line_list:
                    raise Exception("Wrong file")
                first_line = False
            else:
                word_list = line[0:-1].split(",")
                if len(word_list) != elem_count:
                    raise Exception(f"Wrong file:\n Line \'{line}\' should have {elem_count} elements")
                self.movieId.append(word_list[0])
                self.imdbId.append(word_list[1])
                self.tmdbId.append(word_list[2])
        f.close()
    
    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        imdb_info = list()
        for movie in list_of_movies:
            tmp_dict = dict()
            if movie in self.movieId:
                tmp_dict["movieId"] = movie
                imdbId = self.imdbId[self.movieId.index(movie)]
                url = "http://www.imdb.com/title/tt" + imdbId + "/"
                response = requests.get(url).text
                soup = BeautifulSoup(response, 'html.parser')

                blocks = soup.find_all('li', class_="ipc-metadata-list__item")
                for block in blocks:
                    if block.text.find('Director') >= 0 and "Director" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Director'] = group
                    elif block.text.find('Writers') >= 0 and "Writers" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Writers'] = group
                    elif block.text.find('Stars') >= 0 and "Stars" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Stars']= group
                    elif block.text.find('Runtime') >= 0 and "Runtime" in list_of_fields:
                        group = [group.text for group in block.find_all('div')]
                        tmp_dict['Runtime']= group
                    elif block.text.find('Production companies') >= 0 and 'Production companies' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Production companies']= group
                    elif block.text.find('Budget') >= 0 and 'Budget' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Budget']= group
                    elif block.text.find('Gross worldwide') >= 0 and 'Gross worldwide' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Gross worldwide']= group
                    elif block.text.find('Gross worldwide') >= 0 and 'Cumulative Worldwide Gross' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Cumulative Worldwide Gross']= group
                    elif block.text.find('Genres') >= 0 and 'Genres' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Genres']= group
                    elif block.text.find('Also known as') >= 0 and 'Titles' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Titles']= group
                
                tmp_list = list()
                for i in list_of_fields:
                    if i in tmp_dict.keys():
                        tmp_list.append(tmp_dict[i])
                    else:
                        tmp_list.append([" -1"])
                imdb_info.append([movie, tmp_list])

        imdb_info.sort(key=lambda i: int(i[0]), reverse=True)
        imdb_info = list(map(lambda x: x[1], imdb_info))
        return imdb_info

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        directors = dict()
        info = self.get_imdb(movie_id_list, ["Director"])
        for direct_list in info:
            for direct in direct_list[0]:
                if direct in directors.keys():
                    directors[direct] += 1
                else:
                    directors[direct] = 1
        directors = list(directors.items())
        directors.sort(key=lambda i: i[1], reverse=True)

        return dict(directors[0:n])
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        budgets = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Budget'])
        for budget_list in info:
            budgets[budget_list[0][0]] = budget_list[1][0]
        budgets = list(budgets.items())
        budgets.sort(key=lambda i: i[1], reverse=True)
        return dict(budgets[0:n])
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        profits = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Cumulative Worldwide Gross', 'Budget'])
        for profit_list in info:
            profits[profit_list[0][0]] = float(profit_list[1][0][1::].split(" ")[0].replace(",", "")) - float(profit_list[2][0][1::].split(" ")[0].replace(",", ""))
        profits = list(profits.items())
        profits.sort(key=lambda i: i[1], reverse=True)
        return dict(profits[0:n])
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        runtimes = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Runtime'])
        for runtime_list in info:
            runtimes[runtime_list[0][0]] = runtime_list[1][0]
        runtimes = list(runtimes.items())
        runtimes.sort(key=lambda i: i[1], reverse=True)
        return dict(runtimes[0:n])
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        costs = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Budget', 'Runtime'])
        for cost_list in info:
            time = cost_list[2][0]
            if time.find('hour') >= 0:
                time_min = float(time[0: time.find('hour')]) * 60
                if time.find('min') >= 0:
                    time_min += float(time[time.find('hour') + 5::].lstrip().split(" ")[0])
            else:
                time_min = float(time)
            costs[cost_list[0][0]] = float(cost_list[1][0][1::].split(" ")[0].replace(",", "")) / time_min
        costs = list(costs.items())
        costs.sort(key=lambda i: i[1], reverse=True)
        return dict(costs[0:n])
    
    def get_movie_selection_id(self, n:int):
        if n < 1:
            n = len(self.movieId)
        tmp_set = set(self.movieId)
        movie_id = list()
        for i in range(0, n):
            movie_id.append(tmp_set.pop())
        return movie_id
