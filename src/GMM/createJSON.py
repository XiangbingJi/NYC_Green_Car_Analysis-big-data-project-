import json

# data is a list of dicts, which contains weight, mu, sigma
def create(data):
    res = {}
    res['type'] = 'FeatureCollection'
    features = []
    for item in data:
        feature = {}
        feature['type'] = 'Feature'
        properties = {}
        properties['mag'] = item['weight'] * 60
        properties['sigma'] = item['sigma']
        feature['properties'] = properties
        geometry = {}
        geometry['type'] = 'Point'
        content = item['center']
        content.append(0);
        geometry['coordinates'] = content
        feature['geometry'] = geometry
        features.append(feature)
    res['features'] = features
    return res
