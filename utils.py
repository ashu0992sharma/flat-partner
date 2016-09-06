from haystack.query import SearchQuerySet, SQ

import string, time, random, json, re


def raw_search(search_string):
    """

    :return:
    """

    if len(search_string) == 0:
        search_string = " "
    search_string = search_string.strip()
    # articles = SearchQuerySet().using('language_article').filter(SQ(content_auto=search_string)).filter(language=language)
    flats = SearchQuerySet().using('default').filter(SQ(content_auto=search_string))
    flat_ids = [flat.pk for flat in flats]

    # flats = SearchQuerySet().filter(query=search_string, using='flat')

    # flats = models.Flat.objects.filter(message__icontains=search_string)
    # for token in search_string.split(" "):
    #     flats = flats | models.Flat.objects.filter(message__icontains=token)
    return flat_ids


def gen_hash(seed):
    """
    :param seed: seed for random generation
    :return: hash key
    """""
    base = string.ascii_letters + string.digits  # Output hash base: all alphabets and digits
    random.seed(seed)  # Input string as the random seed
    hash_value = ""
    for i in range(15):
        # Generate a 15-character hash by randomly select characters from base
        hash_value += random.choice(base)
    return hash_value


def expires():
    """
        :return: a UNIX style timestamp representing 5 minutes from now
    """
    return int(random.randint(1, 9969) * (time.time() + 300))
