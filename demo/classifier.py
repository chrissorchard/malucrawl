import json


def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
        matrix[zz] = range(zz,zz + l1 + 1)
    for zz in range(0,l2):
        for sz in range(0,l1):
            if s1[sz] == s2[zz]:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
            else:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    return matrix[l2][l1]


def classify_is_sus(database_dict, new_url):
	sus_sum = 0; notsus_sum = 0;
	for k,v in database_dict.items():
		dist = levenshtein(new_url, k)
		if v == 1:
			sus_sum = sus_sum + dist
		else:
			notsus_sum = notsus_sum +dist
	if sus_sum > notsus_sum:
		return True
	else:
		return False




if __name__ == '__main__':
	with open('mal_test_data.json', 'r') as f:
		d = [l for l in f]
		d = '\n'.join(d)
		mal_dict = json.loads(d)
		url = 'http://uk.movies.yahoo.com/features/sdfasf'
		print classify_is_sus(mal_dict, url)