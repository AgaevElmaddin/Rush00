from tags import Tags
from links import Links

def test_tags_most_words():
    f1 = Tags("")
    top_n = f1.most_words(10)
    assert isinstance(top_n, dict)
    assert len(top_n) == 10
    longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
    assert top_n[longes_key] == 16

def test_tags_longest():
    f1 = Tags("")
    top_n = f1.longest(10)
    assert isinstance(top_n, list)
    assert isinstance(top_n[0], str)
    assert len(top_n) == 10
    longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
    assert len(top_n[0]) == 85 and top_n[0] == longes_key

def test_tags_most_words_and_longest():
    f1 = Tags("")
    top_n = f1.most_words_and_longest(10)
    assert isinstance(top_n, list)
    assert isinstance(top_n[0], str)
    assert len(top_n) <= 10
    longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
    assert longes_key in top_n

def test_tags_most_popular():
    f1 = Tags("")
    top_n = f1.most_popular(10)
    assert isinstance(top_n, dict)
    assert len(top_n) == 10
    popular_key = "In Netflix queue"
    assert top_n[popular_key] == 131

def test_tags_with_word():
    f1 = Tags("")
    top_n = f1.tags_with("ab")
    assert isinstance(top_n, list)
    assert isinstance(top_n[0], str)
    assert len(top_n) == 26
    assert top_n[0].find("ab") >= 0

def test_links_get_imdb():
    f1 = Links("")
    info_list = f1.get_imdb(["1", "2"], ["movieId"])
    assert isinstance(info_list, list)
    assert isinstance(info_list[0], list)
    assert int(info_list[0][0]) > int(info_list[1][0])

def test_links_top_directors():
    f1 = Links("")
    top_n = f1.top_directors(3)
    assert isinstance(top_n, dict)

def test_links_most_expensive():
    f1 = Links("")
    top_n = f1.most_expensive(3)
    assert isinstance(top_n, dict)

def test_links_most_profitable():
    f1 = Links("")
    top_n = f1.most_profitable(3)
    assert isinstance(top_n, dict)

def test_links_longest():
    f1 = Links("")
    top_n = f1.longest(3)
    assert isinstance(top_n, dict)

def test_links_top_cost_per_minute():
    f1 = Links("")
    top_n = f1.top_cost_per_minute(3)
    assert isinstance(top_n, dict)

def test_links_get_movie_selection_id():
    f1 = Links("")
    top_n = f1.get_movie_selection_id(3)
    assert isinstance(top_n, list)
    assert isinstance(top_n[0], str)
    assert len(top_n) == 3
