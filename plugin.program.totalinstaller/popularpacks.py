import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://totalxbmc.tv/totalrevolution/Addon_Packs/'
ADDON=xbmcaddon.Addon(id='plugin.program.totalinstaller')
VERSION = "1.0.7"
PATH = "Total Installer"            
    
#-----------------------------------------------------------------------------------------------------------------
def POPULAR():
    link = OPEN_URL('http://totalxbmc.tv/totalrevolution/Addon_Packs/addonpacks.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,'popularwizard',iconimage,fanart,description)
    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

#-----------------------------------------------------------------------------------------------------------------
def POPULARWIZARD(name,url,description):
    choice = xbmcgui.Dialog().yesno(name, 'This will install the '+name, '', 'Are you sure you want to continue?', nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return
    elif choice == 1:
        import downloader
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        dp = xbmcgui.DialogProgress()
        dp.create("Addon Packs","Downloading "+name +" addon pack.",'', 'Please Wait')
        lib=os.path.join(path, name+'.zip')
        try:
            os.remove(lib)
        except:
            pass
            downloader.download(url, lib, dp)
            time.sleep(3)
            dp.update(0,"", "Extracting Zip Please Wait")
            xbmc.executebuiltin("XBMC.Extract(%s,%s)" %(lib,addonfolder))
            dialog = xbmcgui.Dialog()
            dialog.ok("Total Installer", "All Done. Your addons will now go through the update process, it may take a minute or two until the addons are working.")
            xbmc.executebuiltin( 'UpdateLocalAddons' )
            xbmc.executebuiltin( 'UpdateAddonRepos' )
#            xbmc.executebuiltin("LoadProfile(Master user)")

#-----------------------------------------------------------------------------------------------------------------
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
#-----------------------------------------------------------------------------------------------------------------
def AUTO_VIEW(content = ''):
    if not content:
        return

    xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') != 'true':
        return

    if content == 'addons':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('addon_view'))
    else:
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('default-view'))

#-----------------------------------------------------------------------------------------------------------------
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

if mode=='popularwizard': POPULARWIZARD(name,url,description)