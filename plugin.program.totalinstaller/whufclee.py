# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.totalxbmc.tv
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time,xbmcvfs
import plugintools

ADDON_ID = 'plugin.program.totalinstaller'
ADDON    = xbmcaddon.Addon(id=ADDON_ID)
HOME     = ADDON.getAddonInfo('path')
ARTPATH  = xbmc.translatePath(os.path.join(HOME, 'resources', 'art')) + os.sep
YT_ID = "TotalXBMC"
params = plugintools.get_params()
nextpage = xbmc.translatePath(os.path.join('special://home/addons/'+ADDON_ID, 'nextpage.png'))

# Main Video Tutorials menu
def main_list(url):
    plugintools.log(YT_ID+" "+repr(params))

    # On first page, pagination parameters are fixed
    if params.get("url") is None:
        params["url"] = "http://gdata.youtube.com/feeds/api/users/"+YT_ID+"/playlists?start-index=1&max-results=25"


    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry>(.*?)</entry>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)' height='360' width='480' yt:name='hqdefault'/>")
        video_id = plugintools.find_single_match(entry,"<yt\:playlistI[^>]+>([^<]+)</yt\:playlistId>")
        feed="?v=2&alt=rss"
        url = "http://gdata.youtube.com/feeds/api/playlists/"+video_id+feed
        print "FEED_URL::" + url
        # Appends a new item to the xbmc item list
        plugintools.add_item( action="vid_list" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )
    
    # Calculates next page URL from actual URL
    start_index = int( plugintools.find_single_match( params.get("url") ,"start-index=(\d+)") )
    max_results = int( plugintools.find_single_match( params.get("url") ,"max-results=(\d+)") )
    next_page_url = "http://gdata.youtube.com/feeds/api/users/"+YT_ID+"/playlists?start-index=%d&max-results=%d" % ( start_index+max_results , max_results)

    plugintools.add_item( action="main_list" , title=">> Next page" , url=next_page_url,thumbnail=nextpage , folder=True )
    
def vid_list(params):
    data = plugintools.read( params.get("url") )
    # Extract items from feed
    feed = str(data) + "?v=2&alt=rss"
    pattern = ""
    matches = plugintools.find_multiple_matches(feed,"<item>(.*?)</item>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)' height='360' width='480' yt:name='hqdefault'/>")
        video_id = plugintools.find_single_match(entry,"<link>http\://www.youtube.com/watch\?v\=([^\&]+)\&").replace("&amp;","&")

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="vid_list" , title=title , plot=plot , url=play(video_id) ,thumbnail=thumbnail , folder=True )
        
def play(params):
    import yt    
    yt.PlayVideo(url)
