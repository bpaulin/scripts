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

def choose (question, tree):
    if len(tree) == 1:
        choice = 0
    else:
        for index, item in enumerate(tree):
            print "%i - %s"%(index, item.get('title'))
        choice = input(question)
    return tree[choice]

if command == "tv":
    # sections
    url = server+'/library/sections/'
    sections = ET.fromstring(urllib.urlopen(url).read())
    # NOTE: only use first [@type='show']
    section = sections.find("./Directory[@type='show']").get('key')

    # shows
    url = url + section + '/all/'
    shows = ET.fromstring(urllib.urlopen(url).read())
    shows = shows.findall("./Directory")
    show = choose("show number? ", shows)
    print "### %s"%show.get("title")

    # seasons
    url = server+show.get("key")
    seasons = ET.fromstring(urllib.urlopen(url).read())
    seasons = seasons.findall("./Directory")
    season = choose("season number? ", seasons)
    print "### %s"%season.get("title")

    # episode
    url = server+season.get("key")
    episodes = ET.fromstring(urllib.urlopen(url).read())
    episodes = episodes.findall("./Video")
    episode = choose("episode number? ", episodes)
    print "### %s"%episode.get("title")

    # stream
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
        "--quiet",
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
    print "playing %s"%name
    subprocess.call(argsvlc)
