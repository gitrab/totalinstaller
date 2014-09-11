# totalXBMC Installer based on original XBMCHUB.com Addon Installer  Module By: Blazetamer-2013-2014
# Refactored by: Yours Truly 2014!!

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time
import downloader
import extract


ADDON_ID = 'plugin.program.totalinstaller'
BASEURL  = 'http://addons.totalxbmc.com/'
ADDON    = xbmcaddon.Addon(id=ADDON_ID)
HOME     = ADDON.getAddonInfo('path')
ARTPATH  = xbmc.translatePath(os.path.join(HOME, 'resources', 'art')) + os.sep
FANART   = os.path.join(ARTPATH, 'fanart.jpg')


#-----------------------------------------------------------------------------------------------------------------

def PLAYVIDEO(url):
    import yt    
    yt.PlayVideo(url)

#-----------------------------------------------------------------------------------------------------------------

def MAININDEX():
   # addDir('Video Guides', 'none', 'videoguides', 'movies.png')
    if ADDON.getSetting('categories') == 'true':
        addDir('Categories', 'none', 'categories', 'categories2.png')

    if ADDON.getSetting('genre') == 'true':
        addDir('Genres', 'none', 'genres', 'genres.png')

    if ADDON.getSetting('countries') == 'true':
        addDir('Countries', 'none', 'countries', 'countries.png')

    if ADDON.getSetting('repositories') == 'true':
        addDir('Repositories', 'category/repositories/', 'addonlist', 'repositories.png')
    addDir('Search by Addon/Author','http://addons.totalxbmc.com/search/?keyword=','searchaddon', 'Search.png')
    addDir('Update My Addons', 'none', 'update', 'update.png')

#-----------------------------------------------------------------------------------------------------------------

def addCategory(category, alt):    
    if ADDON.getSetting(alt) == 'true':
        addDir(category, 'category/categories2/%s/' % alt, 'addonlist', alt+'.png')   
   
def CATEGORIES():        
    addCategory('Audio Addons',  'audio')
    addCategory('Lyrics Addons', 'lyrics')

    if ADDON.getSetting('metadata') == 'true':
        addDir('Metadata', 'none', 'metadata', 'metadata.png')

    addCategory('Picture Addons', 'pictures')
    addCategory('Program Addons', 'programs')
    addCategory('Screensavers',   'screensaver')
    addCategory('Services',       'services')
    addCategory('Skins',          'skins')
    addCategory('Subtitles',      'subtitles')
    addCategory('Video Addons',   'video')
    addCategory('Weather',        'weather')
    addCategory('Web Interface',  'webinterface') 

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addMeta(meta, alt):    
    if ADDON.getSetting('meta'+alt) == 'true':
        addDir(meta, 'category/categories2/metadata/%s/' % alt, 'addonlist', alt+'.png')  


def METADATA():        
    addMeta('Album Metadata',       'albums')
    addMeta('Artist Metadata',      'artists')
    addMeta('Movie Metadata',       'movies')
    addMeta('Music Video Metadata', 'musicvideos')
    addMeta('TV Metadata',          'tvshows')

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addGenre(genre):
    lower = genre.lower()
    lower = lower.replace(' ', '')

    #special cases
    lower = lower.replace('howto...',     'howto')
    lower = lower.replace('news&weather', 'news')
    lower = lower.replace('technology',   'tech')
    lower = lower.replace('tvshows',      'tv')
    lower = lower.replace('misc.',        'other')  
    lower = lower.replace('xxx',          'adult')

    if ADDON.getSetting(lower) == 'true':
        addDir(genre, 'category/genres/%s/' % lower, 'addonlist', lower+'.png')

def GENRES():       
    addGenre('Anime')
    addGenre('Audiobooks')
    addGenre('Comedy')
    addGenre('Comics')
    addGenre('Documentary')
    addGenre('Downloads')
    addGenre('Food')
    addGenre('Gaming')
    addGenre('Health')
    addGenre('How To...')
    addGenre('Kids')
    addGenre('Live TV')
    addGenre('Movies')
    addGenre('Music')
    addGenre('News & Weather')
    addGenre('Photos')
    addGenre('Podcasts')
    addGenre('Radio')
    addGenre('Religion')
    addGenre('Space')
    addGenre('Sports')
    addGenre('Technology')
    addGenre('Trailers')
    addGenre('TV Shows')
    addGenre('Misc.')
    addGenre('XXX')

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addCountry(country):
    lower = country.lower()
    if ADDON.getSetting(lower) == 'true':
        addDir(country, 'category/countries/%s/' % lower, 'addonlist', lower+'.png')
    
def COUNTRIES():        
     #addCountry('African')
     addCountry('Arabic')
     addCountry('Asian')
     addCountry('Australian') 
     addCountry('Austrian')
     addCountry('Belgian')
     addCountry('Brazilian')
     addCountry('Canadian')
     addCountry('Chinese')
     addCountry('Columbian')
     addCountry('Czech')
     addCountry('Danish')
     addCountry('Dominican')
     addCountry('Dutch')
     addCountry('Egyptian')
     addCountry('Filipino')
     addCountry('Finnish')
     addCountry('French')
     addCountry('German')
     addCountry('Greek')
     addCountry('Hebrew')
     addCountry('Hungarian')
     addCountry('Icelandic')
     addCountry('Indian')
     addCountry('Irish')
     addCountry('Italian')
     addCountry('Japanese')
     addCountry('Korean')
     addCountry('Lebanese')
     addCountry('Mongolian')
     addCountry('Moroccan')
     addCountry('Nepali')
     addCountry('New Zealand')
     addCountry('Norwegian')
     addCountry('Pakistani')
     addCountry('Polish')
     addCountry('Portuguese')
     addCountry('Romanian')
     addCountry('Russian')
     addCountry('Singapore')
     addCountry('Spanish')
     addCountry('Swedish')
     addCountry('Swiss')
     addCountry('Syrian')
     addCountry('Tamil')
     addCountry('Thai')
     addCountry('Turkish')
     addCountry('UK')
     addCountry('USA')
     addCountry('Vietnamese')

     AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def nextPage(link, mode):
    nmatch = re.compile('"page last" href="(.+?)"><dfn title="next Page">').findall(link)
    if len(nmatch) > 0:
        addDir('Next Page', nmatch[0], mode, '')

#-----------------------------------------------------------------------------------------------------------------
    
def REPOLIST(url):
    link  = OPEN_URL(url)
    match = re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)

    for url, image, name, in match:
        if 'repo' in name.lower():
            iconimage = BASERURL + image
            add2HELPDir(name, url, 'addonindex', iconimage, FANART, '', 'addon')
                      
    nextPage(link, 'repolist')    
           
    AUTO_VIEW()    

#-----------------------------------------------------------------------------------------------------------------

def ADDONLIST(url):
    link  = OPEN_URL(url)
    match = re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)

    for url, image, name, in match:
        iconimage = BASEURL + image
        add2HELPDir(name, url, 'addonindex', iconimage, FANART, '', 'addon')                    
        
    nextPage(link, 'addonlist')    

    AUTO_VIEW() 

#-----------------------------------------------------------------------------------------------------------------
    
def ADDONINDEX(name, url, filetype):
    link = OPEN_URL(url)

    videos = re.compile('https://www.youtube.com/watch\?v=(.+?)"target.+?alt="(.+?)" />').findall(link)
    match1 = re.compile('rel="nofollow">(.+?)</a>').findall(link)
#    match1 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match2 = re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)
    match3 = re.compile('class="pic" /></span>\s*<h2>(.+?)</h2>').findall(link)
    match4 = re.compile('Repository:</strong> <a href="(.+?)"').findall(link)
    match5 = re.compile('Description:</h2><h4>(.+?)</h4>').findall(link)
    match6 = re.compile('Download:</strong><br /><a href="(.+?)"').findall(link)
    match7 = re.compile('Author:</strong> <a href=".+?">(.+?)</a>').findall(link)
    match8 = re.compile('Version:</strong>(.+?)<br').findall(link)
    match9 = re.compile('Add-on Type:</strong>(.+?)<br').findall(link)
    match10 = re.compile('Details:</strong>(.+?)</h1').findall(link)
    match11 = re.compile('Notes:</strong>(.+?)<br').findall(link)
    match12 = re.compile('Genres:</strong>(.+?)<br').findall(link)
    match13 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match14 = re.compile('Platform:</strong>(.+?)<br />').findall(link)

    repository1  = match1[0] if (len(match1) > 0) else ''
    image        = match2[0] if (len(match2) > 0) else ''
    name         = match3[0] if (len(match3) > 0) else ''
    repourl      = match4[0] if (len(match4) > 0) else 'none'
    description  = match5[0] if (len(match5) > 0) else 'Description not available at this time'
    addonurl     = match6[0] if (len(match6) > 0) else ''
    author       = match7[0] if (len(match7) > 0) else ''
    version      = match8[0] if (len(match8) > 0) else ''
    addontype    = match9[0] if (len(match9) > 0) else ''
    status       = match10[0] if (len(match10) > 0) else '[COLOR lime]No problems reported[/COLOR]'
    notes        = match11[0] if (len(match11) > 0) else 'None'
    genres       = match12[0] if (len(match12) > 0) else '[COLOR red]No genre information available, please help us categorise this correctly by posting on the forum at totalxbmc.tv[/COLOR]'
    repository2  = match13[0] if (len(match13) > 0) else ''
    platform     = match14[0] if (len(match14) > 0) else '[COLOR red]No platform information available[/COLOR]'
    iconimage    = BASEURL + image
	
#	check if there is a repo link, if not it needs use repository2 otherwise a load of garbage is added to the string
    if len(repository1) < 50:
		showText(name+'   v.'+version, '[COLOR blue]Remember we rely on[/COLOR] [COLOR white]YOU[/COLOR] [COLOR blue]the brilliant XBMC/Kodi Community to keep this info updated.''\nIf any of this information is incorrect please let us know,''\n''just post a report on the forum at[/COLOR] [COLOR lime]www.totalxbmc.tv[/COLOR]\n\n\n''Supported Platforms:  '+platform+'\n\n''Addon Type:  '+addontype+'\n\n''Genre:  '+genres+'\n\n''Developer:  '+author+'\n\n''Repository:  '+repository1+'\n\n''Status:  [COLOR red]'+status+'[/COLOR]\n\n''Notes:  [COLOR yellow]'+notes+'[/COLOR]\n\n''Description:  [COLOR blue]'+description+'[/COLOR]')
    else:
		showText(name+'   v.'+version, '[COLOR blue]Remember we rely on[/COLOR] [COLOR white]YOU[/COLOR] [COLOR blue]the brilliant XBMC/Kodi Community to keep this info updated.''\nIf any of this information is incorrect please let us know,''\n''just post a report on the forum at[/COLOR] [COLOR lime]www.totalxbmc.tv[/COLOR]\n\n\n''Supported Platforms:  '+platform+'\n\n''Addon Type:  '+addontype+'\n\n''Genre:  '+genres+'\n\n''Developer:  '+author+'\n\n''Repository:  '+repository2+'\n\n''Status:  [COLOR red]'+status+'[/COLOR]\n\n''Notes:  [COLOR yellow]'+notes+'[/COLOR]\n\n''Description:  [COLOR blue]'+description+'[/COLOR]')
    addHELPDir('Install '+name, '  (Addon Type:'+addontype+')', addonurl, 'addoninstall', iconimage, FANART, description, 'addon', repourl, version, author)

    for video, name in videos:
        image = 'https://i1.ytimg.com/vi/%s/mqdefault.jpg' % video[:11]
        add2HELPDir(name, video, 'watch_video', image, fanart='', description='', filetype='', isFolder=False)

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------    

def showText(heading, text):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

#-----------------------------------------------------------------------------------------------------------------    

def SEARCHADDON(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Search add-ons" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	ADDONLIST(searchUrl)

	AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------    

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default
#-----------------------------------------------------------------------------------------------------------------    
  
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

    response = urllib2.urlopen(req)
    link     = response.read()

    response.close()

    return link.replace('\r','').replace('\n','').replace('\t','')    

#-----------------------------------------------------------------------------------------------------------------

def TOTALINSTALL(name, url, description, filetype, repourl):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))

    dp   = xbmcgui.DialogProgress()
    dp.create("First Launch:","Creating Database ",'','Only Shown on First Launch')

    lib = os.path.join(path,name+'.zip')

    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    if filetype == 'addon':
        addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))

    time.sleep(2)
    extract.all(lib, addonfolder, '')
    
#-----------------------------------------------------------------------------------------------------------------

def DEPENDINSTALL(name, url):
    files = url.split('/')

    dependname = files[-1:]
    dependname = str(dependname)
    dependname = dependname.replace('[','')
    dependname = dependname.replace(']','')
    dependname = dependname.replace('"','')
    dependname = dependname.replace('[','')
    dependname = dependname.replace("'",'')
    dependname = dependname.replace(".zip",'')

    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp   = xbmcgui.DialogProgress()
    dp.create('Configuring Requirements:', '', 'Downloading and ', 'Installing '+ name)

    lib = os.path.join(path,name+'.zip')
    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))

    time.sleep(2)
    extract.all(lib, addonfolder, '')
        
    depends = xbmc.translatePath(os.path.join('special://home/addons/'+dependname,'addon.xml'))    
    source  = open( depends, mode = 'r' )
    link    = source.read( )
    source.close ( )

    dmatch = re.compile('import addon="(.+?)"').findall(link)
    for requires in dmatch:
        if not 'xbmc.python' in requires:
            print 'Script Requires --- ' + requires
            dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
            if not os.path.exists(dependspath):
                DEPENDINSTALL(requires, 'http://raw.github.com/totalxbmc/modules/master/'+requires+'.zip')

#-----------------------------------------------------------------------------------------------------------------

def ADDONINSTALL(name, url, filetype, repourl):
    print 'Installing Url : ' + url

    confirm = xbmcgui.Dialog().yesno('Please Confirm', '                Do you wish to install the chosen add-on and', '                        its respective repository if needed?', '                    ', 'Cancel', 'Install')  
    if confirm == 0:
        return    

    path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))    

    dp = xbmcgui.DialogProgress()
    dp.create('Download Progress:', 'Downloading your selection', '', 'Please Wait')

    lib = os.path.join(path, name+'.zip')

    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    newfile   = url.split('-')[0:-1]
    newfile   = str(newfile)

    addonname = newfile.split('/')[-1:]
    addonname = str(addonname)
    addonname = addonname.replace('[','')
    addonname = addonname.replace(']','')
    addonname = addonname.replace('"','')
    addonname = addonname.replace('[','')
    addonname = addonname.replace("'",'')

    if filetype == 'addon':
        addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
    elif filetype == 'media':
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
    elif filetype == 'main':
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))

    time.sleep(2)
    extract.all(lib, addonfolder, dp)

    try:
        #Start Addon Depend Search==================================================================
        depends = xbmc.translatePath(os.path.join('special://home/addons/'+addonname, 'addon.xml'))    
        source  = open(depends, mode = 'r')
        link    = source.read()
        source.close ()

        dmatch = re.compile('import addon="(.+?)"').findall(link)
        for requires in dmatch:
            if not 'xbmc.python' in requires:
                dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
                if not os.path.exists(dependspath):
                    DEPENDINSTALL(requires, 'http://raw.github.com/totalxbmc/modules/master/'+requires+'.zip')
    except:
        pass            
        
    if  'none' not in repourl:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
     
        dp = xbmcgui.DialogProgress()
        dp.create('Updating Repo if needed:', 'Configuring Installation', '', '')

        lib = os.path.join(path,name+'.zip')

        try:    os.remove(lib)
        except: pass

        downloader.download(repourl, lib, '')

        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
        elif filetype == 'media':
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
        elif filetype == 'main':
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))

        time.sleep(2)
        extract.all(lib, addonfolder, dp)
    xbmc.executebuiltin( 'UpdateAddonRepos' )            
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmcgui.Dialog().ok('Success! Your selection has now been installed', 'If you like what we\'re creating at totalxbmc.tv please come', 'and make yourself know on the forum. All donations are very', 'welcome and will go towards the running costs. Thank you!')

#-----------------------------------------------------------------------------------------------------------------

def UPDATEREPO():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Success! Update process will now take place', 'If you like what we\'re creating at totalxbmc.tv please come', 'and make yourself know on the forum. All donations are very', 'welcome and will go towards the running costs. Thank you!')

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

def addDir(name, url, mode, iconimage = ''): 
    if len(iconimage) > 0:
        iconimage = ARTPATH + iconimage
    else:
        iconimage = 'DefaultFolder.png'

    if url.lower() != 'none':
        if not url.startswith(BASEURL):
            url = BASEURL + url

    u  = sys.argv[0]
    u += "?url="  + urllib.quote_plus(url)
    u += "&name=" + urllib.quote_plus(name)
    u += "&mode=" + str(mode)

    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

    liz.setProperty("Fanart_Image", FANART )
    
    addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

#-----------------------------------------------------------------------------------------------------------------

def addHELPDir(name, addontype, url, mode, iconimage, fanart, description, filetype, repourl='', version='', author=''):
        u  = sys.argv[0]
        u += "?url="         + urllib.quote_plus(url)
        u += "&name="        + urllib.quote_plus(name)
        u += "&filetype="    + urllib.quote_plus(filetype)
        u += "&repourl="     + urllib.quote_plus(repourl)
        u += "&mode="        + str(mode)
                        
        liz = xbmcgui.ListItem(name+addontype, iconImage='DefaultFolder.png', thumbnailImage=iconimage)

        liz.setInfo(type="Video", infoLabels={ 'title': name, 'plot': description } )
        liz.setProperty('Fanart_Image', fanart )

        liz.setProperty('Addon.Description', description )
        liz.setProperty('Addon.Creator', author )
        liz.setProperty('Addon.Version', version )        

        addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)

#-----------------------------------------------------------------------------------------------------------------

def add2HELPDir(name, url, mode, iconimage, fanart, description, filetype, isFolder=True):
        u  = sys.argv[0]
        u += "?url="         + urllib.quote_plus(url)
        u += "&name="        + urllib.quote_plus(name)
        u += "&filetype="    + urllib.quote_plus(filetype)
        u += "&mode="        + str(mode)
        
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

        liz.setInfo(type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty("Fanart_Image", fanart )

        addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

#-----------------------------------------------------------------------------------------------------------------  

def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
    
#-----------------------------------------------------------------------------------------------------------------
    
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

#-----------------------------------------------------------------------------------------------------------------

params = get_params()

try:    mode = urllib.unquote_plus(params['mode'])
except: mode = None

try:    url = urllib.unquote_plus(params['url'])
except: url = ''

try:    name = urllib.unquote_plus(params['name'])
except: name = ''

try:    type = urllib.unquote_plus(params['filetype'])
except: type = ''

try:    repo = urllib.unquote_plus(params['repourl'])
except: repo = ''

if 'repo' in name.lower() and len(repo) > 0:
    url = repo


#print "Mode : " + str(mode)
#print "URL  : " + str(url)
#print "Name : " + str(name)
#print "Repo : " + str(repo)
#print "Type : " + str(type)


if mode   == None            : MAININDEX()
elif mode == 'categories'    : CATEGORIES()
elif mode == 'metadata'      : METADATA()
elif mode == 'genres'        : GENRES()
elif mode == 'countries'     : COUNTRIES()
elif mode == 'update'        : UPDATEREPO()
elif mode == 'addonlist'     : ADDONLIST(url)
elif mode == 'repolist'      : REPOLIST(url)
elif mode == 'addonindex'    : ADDONINDEX(  name, url, type)
elif mode == 'addoninstall'  : ADDONINSTALL(name, url, type, repo)
elif mode == 'watch_video'   : PLAYVIDEO(url)
elif mode == 'runvids'       : UPDATEREPO()
elif mode == 'totalvids'     : TOTALVIDS(params)
elif mode == 'searchaddon'   : print""+url; SEARCHADDON(url)

else:
    MAININDEX()

xbmcplugin.endOfDirectory(int(sys.argv[1]))