import json
d = {"one":1, "two":2}
json.dump(d, open("./templates/map.json",'w'))
d2 = json.load(open("./templates/map.json"))
print d2
