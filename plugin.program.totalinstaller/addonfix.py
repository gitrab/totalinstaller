#
#      Copyright (C) 2014 Richard Dean
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time

def fixes():
    link = OPEN_URL('http://totalxbmc.tv/totalrevolution/Addon_Fix/addonfix.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDirfix(name,url,'OSS',iconimage,fanart,description)       
 #       else:
#			addDirfix(name,url,'copyfile',iconimage,fanart,description,addonid,filepath)

#def COPYFILE(name,addonid,url,filepath,iconimage,description):
#    datapath = xbmc.translatePath(addonid.getAddonInfo('profile'))
#    if os.path.exists(datapath):
#        path = localini
#        try:
#            urllib.urlretrieve(url, filepath)
#        except:
#            pass
#    else:
#        d = xbmcgui.Dialog()
#        d.ok('OnTapp.TV is not installed.', 'Please visit www.on-tapp.tv for information.')

def OSS(name,url,iconimage,description):
    ADDON    = xbmcaddon.Addon(id = 'script.tvguidedixie')
    datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    #RD change below
    localini = os.path.join(datapath, 'local.ini')
    choice = xbmcgui.Dialog().yesno('OffsideStreams / OnTapp.TV Integration ', description, nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return
    elif choice == 1:
        path = localini
        if not os.path.exists(datapath):
            d = xbmcgui.Dialog()
            d.ok('[COLOR=red]OnTapp Not Installed[/COLOR]','The On-Tapp.TV addon has not been found on this system, please install then run this again.')
#Might try and give the option to install OTTV if not installed.
#            ADDONINDEX('OnTapp.TV','http://addons.totalxbmc.com/show/script.tvguidedixie/','addon')
        else:
            urllib.urlretrieve(url, path)
            d = xbmcgui.Dialog()
            d.ok('OSS Integration complete', 'The OffsideStreams local.ini file has now been copied to your OnTapp.TV directory')

        
def addDirfix(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

params=get_params()
url=None
name=None
addonid=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        addonid=urllib.unquote_plus(params["addonid"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
                
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "Addon ID: "+str(addonid)
print "description: "+str(description)

if mode == 'copyfile'     : COPYFILE(name,addonid,url,filepath,iconimage,description)
elif mode == 'OSS'        : OSS(name,url,iconimage,description)