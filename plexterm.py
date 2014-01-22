#!/usr/bin/python
# quick&dirty script to play a video from plexserver with vlc
import xml.etree.ElementTree as ET
import urllib
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Open plex media')
parser.add_argument('--server', metavar='SERVER', type=str, action="store", help='server ip', default='http://localhost:32400')
parser.add_argument('id', metavar='ID', type=str, action="store", help='media id')
args = vars(parser.parse_args())
server = args['server']
id = args['id']

try:
    url = server+'/library/metadata/'+str(id)
    metadata = urllib.urlopen(url).read()
except Exception, e:
    print "Can't read from "+url
else:
    tree = ET.fromstring(metadata)
    video = tree.find("./Video/Media/Part").get('key')
    argsvlc = [
        "vlc",
        "--qt-minimal-view",
        server+video
    ]
    try:
        sub = tree.find("./Video/Media/Part/Stream[@format='srt']").get('key')
        argsvlc.append("--sub-file="+server+sub)
    except Exception, e:
        print "no subs"
    subprocess.call(argsvlc)
    print "Hello, World!"
