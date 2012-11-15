from pebl.util import levenshtein


_mal_list = []


def classify_is_sus(database, new_url):
    sus_sum = 0
    notsus_sum = 0
    sind = 1
    nind = 1
    for item in database:
        dist = levenshtein(new_url, item["url"])
        if item["malware"]:
            sus_sum = sus_sum + dist
            sind = sind + 1
        else:
            notsus_sum = notsus_sum + dist
            nind = nind + 1
    avg_sus = sus_sum/sind
    avg_notsus = notsus_sum/nind
    total_len = avg_sus + avg_notsus
    if avg_sus > avg_notsus:
        return False, 1.0 - float(avg_notsus)/float(total_len)
    else:
        return True, 1.0 - float(avg_sus)/float(total_len)


def add_url(url, is_mal):
    """ Gets url and if it is a malware and fills the 
        _mal_list which is used for the classification task

        url -- the url which is classified as malware or not 
        is_mal -- true or false 
    """
    global _mal_list
    _mal_list.append ({"url":url, "malware":is_mal})

if __name__ == '__main__':
    import json
    import pkgutil
    mal_dict = json.loads(pkgutil.get_data("classifier", "mal_test_data.json"))
    url = 'http://uk.movies.yahoo.com/features/sdfasf'
    print classify_is_sus(mal_dict, url)