import urllib2
from urllib2 import urlopen
import json
f = open('streets_wholefoods.txt')
lines = f.readlines()

coords = []

for line in lines:
        url = 'http://maps.google.com/maps/api/geocode/json?address='
        url += urllib2.quote(line.rstrip()) + "&sensor=false"
        status = "BAD"
        while (status != "OK"):
                data = json.loads(urlopen(url).read())
                status = data["status"]
        coord = data["results"][0]["geometry"]["location"]
        coord["address"] = line.rstrip()
        coords.append(coord)
        print url
        print len(coords)
        
#print coords
f.close()

f2 = open("coords_wholefoods.json", "w+")
f2.write(json.dumps(coords))
f2.close()
