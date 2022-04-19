from collections import Counter

class Tags:
    """
    Analyzing data from tags.csv
    """
    first_line_list = ["userId","movieId","tag","timestamp"]
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        f = open(path_to_the_file + "tags.csv", "r")
        self.userId = list()
        self.movieId = list()
        self.tag = list()
        self.timestamp = list()
        first_line = True
        elem_count = len(self.first_line_list)
        for line in f:
            if first_line:
                word_list = line[0:-1].split(",")
                if word_list != self.first_line_list:
                    raise Exception("Wrong file")
                first_line = False
            else:
                word_list = line.split(",")
                if len(word_list) != elem_count:
                    raise Exception(f"Wrong file:\n Line \'{line}\' should have {elem_count} elements")
                self.userId.append(word_list[0])
                self.movieId.append(word_list[1])
                self.tag.append(word_list[2])
                self.timestamp.append(word_list[3])
        f.close()


    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
 where the keys are tags and the values are the number of words inside the tag.
 Drop the duplicates. Sort it by numbers descendingly.
        """
        if n < 1:
            n = -1
        big_tags = set(map(lambda x: (x,len(x.split(" "))), self.tag))
        big_tags = list(big_tags)
        big_tags.sort(key=lambda i: i[1], reverse=True)
        big_tags = dict(big_tags[0:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        if n < 1:
            n = -1
        big_tags = set(map(lambda x: (x,len(x)), self.tag))
        big_tags = list(big_tags)
        big_tags.sort(key=lambda i: i[1], reverse=True)
        big_tags = list(map(lambda x: x[0], big_tags[0:n]))
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        most_words_list = self.most_words(n)
        tags_key = most_words_list.keys()
        longest_list = self.longest(n)
        big_tags = list(set(tags_key).intersection(set(longest_list)))
        return big_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        if n < 1:
            n = -1
        popular_tags = list(set(Counter(self.tag).items()))
        popular_tags.sort(key=lambda i: i[1], reverse=True)
        popular_tags = dict(popular_tags[0:n])
        return popular_tags
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        unique_tags = set(self.tag)
        tags_with_word = list(filter(lambda x: x.find(word) >= 0, unique_tags))
        tags_with_word.sort()
        return tags_with_word
