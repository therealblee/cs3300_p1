import simplejson, urllib

KEY = "AIzaSyAAYP3vtxZ59mAZ2n2pjXEi4SuhERu3K34" #not used
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?address='

addresses = "" #name of file of human-readable addresses
results = "geocodes.txt"

fp2 = open(results, "w")

with open(addresses) as f:
	for line in f:
		# example line:
		# line = "121 Oxenbridge Rd, Quincy, MA"
		#format line into url
		array = line.split(' ')
		query = '+'.join(array)
		url = GEOCODE_BASE_URL+query+"&sensor=false" #need sensor=false if not viewing on a mobile device
		#make API call aka open url to the address and get a big ass json object.
		result = simplejson.load(urllib.urlopen(url))
		coords = 'lat:%f, lng:%f' %(result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng'])
		#write to fp2
		#each line is supposed to be the address followed by lat, lng
		fp2.write(line+" "+coords+"\n")

fp2.close()