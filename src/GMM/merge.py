import json
import csv

csv.register_dialect(
	'mydialect',
	delimiter = ',',
	quotechar = '"',
	doublequote = True,
	skipinitialspace = True,
	lineterminator = '\r\n',
	quoting = csv.QUOTE_MINIMAL)

outputPath = './mergedData.json'
res = []
for i in range(24):
	first = True
	inputPath = './output/Output' + str(i) + '.json'
	with open(inputPath, 'rb') as mycsvfile:
		tmp = []
		json1_file = open(inputPath)
		json1_str = json1_file.read()
		json1_data = json.loads(json1_str)
		features = json1_data['features']
		for item in features:
			feature = {}
			item['geometry']['coordinates'].remove(0)
			feature['coordinates'] = item['geometry']['coordinates']
			feature['mag'] = item['properties']['mag'] / 60
			feature['sigma'] = item['properties']['sigma']
			tmp.append(feature)
		res.append(tmp)

with open(outputPath, 'w') as outfile:
	json.dump(res, outfile, sort_keys = False, indent = 4, separators = (',', ':'))