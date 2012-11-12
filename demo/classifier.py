from pebl.util import levenshtein


def classify_is_sus(database_dict, new_url):
    sus_sum = 0
    notsus_sum = 0
    sind = 0
    nind = 0

    for k, v in database_dict.items():
        dist = levenshtein(new_url, k)
        if v == 1:
            sus_sum = sus_sum + dist
            sind = sind + 1
        else:
            notsus_sum = notsus_sum + dist
            nind = nind + 1

    avg_sus = sus_sum / sind
    avg_notsus = notsus_sum / nind

    if avg_sus > avg_notsus:
        return False
    else:
        return True


if __name__ == '__main__':
    import json
    import pkgutil

    mal_dict = json.loads(pkgutil.get_data("classifier", "mal_test_data.json"))
    url = 'http://uk.movies.yahoo.com/features/sdfasf'
    print classify_is_sus(mal_dict, url)
