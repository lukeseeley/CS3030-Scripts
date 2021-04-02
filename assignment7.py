import json
from urllib.request import urlopen

url = "https://content.services.pbskids.org/v2/kidspbsorg/home"
response = urlopen(url)

data = json.loads(response.read())
#print(data['collections']['kids-programs-tier-1'])

programs = []
for homekey in data['collections']:
    homesubkeys = homekey.split('-')
    if(homesubkeys[1] == 'programs'):
        for program in data['collections'][homekey]['content']:
            programs.append(program)

count = 0
print("\nAvailable PBS Kids TV series:")
for program in programs:
    print(str(count) + ": " + program['title'])
    count += 1

seriesNumber = input("Enter the number of the TV series you would like to select: ")
series = programs[int(seriesNumber)]

rawurl = series['URI']
spliturl = rawurl.split('/')
seriesurl = "https://content.services.pbskids.org/" + "/".join(spliturl[3:])
#print(seriesurl)
seriesresponse = urlopen(seriesurl)

seriesdata = json.loads(seriesresponse.read())
rawepisodes = seriesdata['collections']['episodes']['content']
episodes = []
for episode in rawepisodes:
    episodes.append(episode)

count = 0
print("\nAvailable episodes for the " + series['title'] + " series:")
for episode in episodes:
    print(str(count) + ": " + episode['title'])
    count += 1

episodeNumber = input("Enter a number for the desired episode: ")
episode = episodes[int(episodeNumber)]

print("\nThe episode URL: " + episode['URI'])