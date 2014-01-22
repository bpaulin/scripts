#!/usr/bin/python
# quick&dirty script to play a video from plexserver with vlc
import xml.etree.ElementTree as ET
import urllib
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Open plex media')
parser.add_argument('--server', metavar='SERVER', type=str, action="store", help='server ip', default='http://localhost:32400')
parser.add_argument('command', metavar='ID', type=str, action="store", help='media id')
args = vars(parser.parse_args())
server = args['server']
command = args['command']

if command == "tv":
    # sections
    url = server+'/library/sections/'
    sections = ET.fromstring(urllib.urlopen(url).read())
    # NOTE: only use first [@type='show']
    section = sections.find("./Directory[@type='show']").get('key')
    url = url + section + '/all/'
    # shows
    shows = ET.fromstring(urllib.urlopen(url).read())
    shows = shows.findall("./Directory")
    for index, show in enumerate(shows):
        print "%i - %s"%(index, show.get('title'))
    choice = 'wrong'
    choice = input("show number? ")
    print "### %s"%shows[choice].get("title")
    # seasons
    show = shows[choice]
    url = server+show.get("key")
    seasons = ET.fromstring(urllib.urlopen(url).read())
    seasons = seasons.findall("./Directory")
    for index, season in enumerate(seasons):
        print  "%i - %s"%(index, season.get('title'))
    choice = input("season number? ")
    print "## %s"%seasons[choice].get("title")
    # episode
    season = seasons[choice]
    url = server+season.get("key")
    episodes = ET.fromstring(urllib.urlopen(url).read())
    episodes = episodes.findall("./Video")
    for index, episode in enumerate(episodes):
        print  "%i - %s"%(index, episode.get('title'))
    choice = input("episode number? ")
    print "# %s"%episodes[choice].get("title")
    # stream
    episode = episodes[choice]
    key = episode.get("key")
else:
    key = '/library/metadata/'+str(command)

# playing file
try:
    url = server+key
    metadata = urllib.urlopen(url).read()
except Exception, e:
    print "Can't read from "+url
else:
    tree = ET.fromstring(metadata)
    video = tree.find("./Video/Media/Part").get('key')
    # Common args
    argsvlc = [
        "cvlc",
        "--qt-minimal-view",
        server+video
    ]
    # Subtitle
    try:
        sub = tree.find("./Video/Media/Part/Stream[@format='srt']").get('key')
        argsvlc.append("--sub-file="+server+sub)
    except Exception, e:
        print "no subs"
    # window title
    name = tree.find("./Video").get('title')
    if (tree.find("./Video").get('type') == "episode"):
         name = (tree.find("./Video").get('grandparentTitle')+
                ' - s' +
                tree.find("./Video").get('parentIndex') +
                'e' +
                tree.find("./Video").get('index') +
                ' - ' +
                name)
    argsvlc.append("--video-title="+name)
    # launch vlc
    subprocess.call(argsvlc)
