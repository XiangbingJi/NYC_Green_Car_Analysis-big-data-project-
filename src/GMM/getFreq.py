import json, sys
import functools

def compare(x1, x2):
    one = x1['properties']['mag']
    two = x2['properties']['mag']
    if one == two:
        return 0
    elif one < two:
        return 1
    else:
        return -1

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def findNearest(features):
    result = {}
    for key in coor:
        minValue = sys.maxint
        for i in range(3):
            d = dist(features[i]['geometry']['coordinates'], coor[key])
            if(d < minValue):
                result[key] = i
                minValue = d
    return result

def dist(p1, p2):
    return (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])



prefix = './output/Output'
totalNum = [66091, 49900, 69738, 24356, 21575, 16770, 22896, 40171, 58716, 60246, 55371, 56615, 57832, 58310, 67355, 74096, 78908, 85783, 94628, 89682, 68142, 71992, 74337, 76085]
coor = {}
coor['Manhattan'] = [-73.95, 40.80]
coor['Queens'] = [-73.89, 40.74]
coor['Brooklyn'] = [-73.98, 40.68]
res = []
for i in range(24):
    tmp = {}
    tmp['timezone'] = i
    path = prefix + str(i) + '.json'
    json1_file = open(path)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    features = json1_data['features']

    features = sorted(features, key =cmp_to_key(compare))
    near = findNearest(features)
    dict = {}
    dict['Manhattan'] = (int)(features[near['Manhattan']]['properties']['mag'] / 60 * totalNum[i])
    dict['Queens'] = (int)(features[near['Queens']]['properties']['mag'] / 60 * totalNum[i])
    dict['Brooklyn'] = (int)(features[near['Brooklyn']]['properties']['mag'] / 60 * totalNum[i])

    tmp['freq'] = dict
    res.append(tmp)

with open('freq.json', 'w') as outfile:
    json.dump(res, outfile, sort_keys = False, indent = 4)

