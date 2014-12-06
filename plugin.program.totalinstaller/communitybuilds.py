import sys,xbmcaddon,xbmcgui,xbmcplugin,xbmc,os,subprocess
import urllib2,urllib
import re
import extract
import downloader
import time
import backuprestore

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://totalxbmc.com/playground/TI_Community_Builds/'
ADDON=xbmcaddon.Addon(id='plugin.program.totalinstaller')
VERSION = "1.0.7"
PATH = "Total Installer"            
linux = xbmc.executebuiltin("System.Platform.Linux")
windows = xbmc.executebuiltin("System.Platform.Windows")
OSX = xbmc.executebuiltin("System.Platform.Darwin")
ATV = xbmc.executebuiltin("System.Platform.ATV2")
zip = ADDON.getSetting('zip')

def COMMUNITY():
    if zip == '':
        dialog.ok('USB BACKUP/RESTORE','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    link = OPEN_URL('http://totalxbmc.tv/totalrevolution/Community_Builds/community_builds.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,'communitywizard',iconimage,fanart,description)
    setView('movies', 'MAIN')
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    if zip == '':
        dialog.ok('USB BACKUP/RESTORE','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    choice = xbmcgui.Dialog().yesno('The ' +name +' build', description, 'Would you like to install?', nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return
    elif choice == 1:
#        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        dp = xbmcgui.DialogProgress()
        dp.create("Community Builds","Downloading "+name +" build.",'', 'Please Wait')
        lib=os.path.join(zip, 'backup.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib, dp)
        backuprestore.RESTORE()
        time.sleep(3)
        dp.update(0,"Download Complete", "Extracting Zip Please Wait")
#        xbmc.executebuiltin("XBMC.Extract(%s,%s)" %(lib,addonfolder))
        dialog = xbmcgui.Dialog()
        dialog.ok("Community Builds", "Install Complete", "To ensure the skin settings are set correctly XBMC will now close. If you would like to upload your build for the community visit the forum at [COLOR=lime][B]www.totalxbmc.tv[/B][/COLOR]")
        if 'win32' in sys.platform:
            killwindows()
        elif 'linux' in sys.platform:
            killlinux()
        elif 'darwin' in sys.platform:
            killatv()
        else: 
            killandroid()

#---------------------------------------------------------------------------------------------------
# Kill Commands - these will make sure guisettings.xml sticks
def killwindows():
        os.system('@ECHO off')
        os.system('TASKKILL /im XBMC.exe /f')
# Possible alternative for older builds - windows tskill XBMC.exe

def killlinux():
        os.system('killall -9 xbmc.bin')        

def killlatv():
        os.system('killall AppleTV')

def killraspbmc():
        os.system('sudo initctl stop xbmc')
        
def killandroid():
        os.system('adb shell ps | grep org.xbmc | awk ''{print $2}'' | xargs adb shell kill')
        
#---------------------------------------------------------------------------------------------------

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
         
def get_params():    
    if len(sys.argv[2]) < 2:
        return []

    param = []

    params        = sys.argv[2]
    cleanedparams = params.replace('?','')

    if (params[len(params)-1] == '/'):
        params = params[0:len(params)-2]

    pairsofparams = cleanedparams.split('&')
    param         = {}

    for i in range(len(pairsofparams)):
        splitparams = {}
        splitparams = pairsofparams[i].split('=')

        if (len(splitparams)) == 2:
            param[splitparams[0]] = splitparams[1]

    return param
  
params=get_params()
url=None
name=None
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
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=str(params["mode"])
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
                
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
if mode == 'communitywizard' : wizard(name,url,description)
